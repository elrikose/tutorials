# Falco

[Falco](https://falco.org/) is a Kubernetes utility that detects security threats in real time:

>Falco is a cloud-native security tool designed for Linux systems. It employs custom rules on kernel events, which are enriched with container and Kubernetes metadata, to provide real-time alerts. Falco helps you gain visibility into abnormal behavior, potential security threats, and compliance violations, contributing to comprehensive runtime security.

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

Copy the falco rules into `/etc/falco/falco_rules.yaml`, edit them and then restart the service.

```sh
cd /etc/falco
vi falco_rules.yaml 
vi /etc/falco/falco_rules.local.yaml 
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
