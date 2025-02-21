# CKS Cheatsheet

This list a bunch of command-line items that are useful for certain topics:

# kube-bench

```sh
# Run against Kubernetes 1.31 security
kube-bench run --version 1.31

# Run kube-bench against a particular code:
kube-bench run -c 1.3.2

# Run against different targets
kube-bench run --targets master --version 1.31
kube-bench run --targets node --version 1.31
kube-bench run --targets controlplane --version 1.31
kube-bench run --targets etcd --version 1.31
kube-bench run --targets policies --version 1.31
```

# /proc

Run all of these as `root` or under `sudo`:

```sh
# Get the PID of a process
$ ps
    PID TTY          TIME CMD
 186565 pts/6    00:00:02 zsh

# Navigate to the folder via its PID
cd /proc/186565

# The executable link
$ ls -ld exe
lrwxrwxrwx 1 barca 0 Feb 20 08:40 exe -> /usr/bin/zsh*

# List open files
$ ls -l ./fd
total 0
lr-x------ 1 barca 64 Feb 20 21:08 12 -> /usr/share/zsh/functions/Completion.zwc
lr-x------ 1 barca 64 Feb 20 21:08 14 -> /usr/share/zsh/functions/Completion/Base.zwc
lr-x------ 1 barca 64 Feb 20 21:08 15 -> /usr/share/zsh/functions/Misc.zwc
l-wx------ 1 barca 64 Feb 20 21:08 19 -> /home/barca/.vscode-server/data/logs/20250220T084006/ptyhost.log
...

# In a container, the root file system
ls -l ./root

# In a container, list the environment variables:
cat ./environ
```


# strace

Run all of these as `root` or under `sudo`:

```sh
# Run a program directly
strace ls -l

# Get a count and summary of calls
strace -cw ls -l

# For a running process
strace -p 1234

# Follow forks of the process
strace -f ls -l
```

# systemctl

Run all of these as `root` or under `sudo`:

```sh
# List all services
systemctl list-units --type=service

# Start a service
systemctl start falco

# Stop a service
systemctl stop falco

# Restart a service
systemctl restart falco

# Is service running
systemctl status falco

# Enable/disable a service to run across reboots
systemctl enable falco
systemctl disable falco
```


# trivy

```sh
# Helpful to get a list of all images in a namespace:
kubectl get pods -n ns -o='custom-columns=NAME:metadata.name,IMAGE:spec.containers[*].image'
```

```sh
# Run and get all security levels
trivy image nginx:1.20.2-alpine

# Run only getting the CRITICAL level
trivy image -s CRITICAL nginx:1.20.2-alpine

# Run only getting the CRITICAL level that match CVE-1234 and CVE-5678
trivy image -s CRITICAL nginx:1.20.2-alpine | grep -e "CVE-1234" -e "CVE-5678"
```
