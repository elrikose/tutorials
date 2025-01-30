# Falco

[Falco](https://falco.org/) is a Kubernetes utility that detects security threats in real time:

>Falco is a cloud-native security tool designed for Linux systems. It employs custom rules on kernel events, which are enriched with container and Kubernetes metadata, to provide real-time alerts. Falco helps you gain visibility into abnormal behavior, potential security threats, and compliance violations, contributing to comprehensive runtime security.

- Part of the CNCF
- Deep Kernel Tracing of the Linux Kernel
- Detect unwanted behavior

Installation:
https://falco.org/docs/install-operate/installation/

Once done you can tail the falco in the `syslog`:

```sh
tail -f /var/log/syslog | grep falco
```

Config file:

```sh
/etc/falco/falco.yaml
```

Rules file:

```sh
/etc/falco/falco_rules.yaml
```

Check to see if Falco is running:

```sh
sudo systemctl status falco
```

Dump out Falco logs. It can tell you where the rules are configured:

```sh
$ cat /var/log/syslog | grep falco
...
Feb 10 21:17:08 controlplane falco: Loading rules from file /etc/falco/falco_rules.yaml:
...
```

On Ubuntu systems you can also use `journalctl`:

```sh
# journalctl -u falco-kmod -f
-- Logs begin at Tue 2025-01-28 07:16:40 EST. --
Jan 30 16:19:16 worker falco[624339]: Loading rules from:
Jan 30 16:19:16 worker falco[624339]:    /etc/falco/falco_rules.yaml | schema validation: ok
Jan 30 16:19:16 worker falco[624339]:    /etc/falco/falco_rules.local.yaml | schema validation: none
Jan 30 16:19:16 worker falco[624339]: The chosen syscall buffer dimension is: 8388608 bytes (8 MBs)
Jan 30 16:19:16 worker falco[624339]: Starting health webserver with threadiness 2, listening on 0.0.0.0:8765
Jan 30 16:19:16 worker falco[624339]: Loaded event sources: syscall
Jan 30 16:19:16 worker falco[624339]: Enabled event sources: syscall
Jan 30 16:19:16 worker falco[624339]: Opening 'syscall' source with Kernel module
```

**Copy** all the falco rules from `/etc/falco/falco_rules.yaml` into `/etc/falco/falco_rules.localyaml`, edit them and then restart the service. NOTE: You MUST copy the file or the local won't have all of the macros loaded and the falco_rules.yaml will be reset.

```sh
cd /etc/falco
cp falco_rules.yaml falco_rules.local.yaml
vi /etc/falco/falco_rules.local.yaml

# Edit the rule
```

And then restart

```sh
sudo systemctl restart falco
sudo systemctl status falco
```

If there is a rule that shows shelling into a container:

```sh
kubectl exec -it pod -- sh
cat /var/log/syslog | grep falco | grep shell
```

## Exercise

Change falco rule to get custom output format:

- Rule: "A shell was spawned in a container with an attached terminal"
- Output Format: "TIME, USER-NAME, CONTAINER-NAME, CONTAINER-ID"
- Priority: Warning

Find the rule in `/etc/falco/falco_rules.yaml`.

```sh
$ grep "A shell was spawned" /etc/falco/falco_rules.yaml
  output: A shell was spawned in a container with an attached terminal (evt_type=%evt.type user=%user.name user_uid=%user.uid user_loginuid=%user.loginuid process=%proc.name proc_exepath=%proc.exepath parent=%proc.pname command=%proc.cmdline terminal=%proc.tty exe_flags=%evt.arg.flags %container.info)
```

Copy the rule into `/etc/falco/falco_rules.local.yaml` and then change both `output:` and `priority:`.

```yaml
- rule: A shell was spawned in a container with an attached terminal
  desc: >
    A shell was used as the entrypoint/exec point into a container with an attached terminal. Parent process may have
    legitimately already exited and be null (read container_entrypoint macro). Common when using "kubectl exec" in Kubernetes.
    Correlate with k8saudit exec logs if possible to find user or serviceaccount token used (fuzzy correlation by namespace and pod name).
    Rather than considering it a standalone rule, it may be best used as generic auditing rule while examining other triggered
    rules in this container/tty.
  condition: >
    spawned_process
    and container
    and shell_procs
    and proc.tty != 0
    and container_entrypoint
    and not user_expected_terminal_shell_in_container_conditions
  output: %evt.time,%user.name,%container.info,%container.id
  priority: WARNING
  tags: [maturity_stable, container, shell, mitre_execution, T1059]
```

# Install on Linux (Ubuntu)

Instructions on how to install Falco onto linux:
https://falco.org/docs/getting-started/falco-linux-quickstart/

```sh
curl -fsSL https://falco.org/repo/falcosecurity-packages.asc | \
sudo gpg --dearmor -o /usr/share/keyrings/falco-archive-keyring.gpg

sudo apt update -y

# Install Dependencies
sudo apt install -y dkms make linux-headers-$(uname -r) dialog

# Install falco
sudo apt install -y falco
```

# Install on Kubernetes

Instructions on how to install Falco into the cluster:
https://falco.org/docs/getting-started/falco-kubernetes-quickstart/

```sh
# Add Helm repo
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

# Deploy Chart
helm install falco -n falco --set driver.kind=ebpf --set tty=true falcosecurity/falco --create-namespace
```

Uninstall

```sh
helm uninstall falco -n falco
kubectl delete ns falco
```
