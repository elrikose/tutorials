# CKS Cheatsheet

This list a bunch of command-line items that are useful for certain topics. Here is what you should enter into the shell to simplify most executions

```sh
# Dry-run Output
export DO='--dry-run=client -o yaml'
# Apply files
alias kaf='kubectl apply -f'
# Delete resource quickly
alias kdel='kubectl delete --grace-period=0 --force'
```

Then you can use them like so:

```sh
kubectl run nginx --image=nginx $DO > nginx.yaml
kaf nginx.yaml
kdel pod nginx
```

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

# sha512sum

```sh
# Single item
$ sha512sum kube-apiserver
da62a165c9243470af47e981c3c929af477cda2d40f8b00227456b71f32d08549578d28630917d7c60e5b80744862e006cb4de3ea8fc92211bcfefb30036ea3c  kube-apiserver

# Multiple items in the same folder
$ sudo sha512sum *
6b41a5ba4cc7e48928fb6b1415c4caf4f3055af4208a2fc9494e8767ad6f0f2365d8e850dd034859ae3df4fedacb1aed757c2d0fd530a1db7ea27f6423f9c8cb  etcd.yaml
875dc823484c3193e245b88455f80b7318579be9d34ddfcc2060094634bdc2b087311a3527a9dbd7dd99cd3b9454cf36323325fb9284f832f5e1453d534ad76d  kube-apiserver.yaml
b02faaeb3fc367fc1d6dc8e089eb5bfd3ba80dbddf769cd3d7cc5cca5584bfa190d8cd4fa01884672d0d11d401812471981147f28c1aeab771b79d8162001ff8  kube-controller-manager.yaml
127218afa7b07977cecb3020bbc89064f463d0b1e6382876be807b95c200fcd8d6948e9e74e1cd120fe888198e126fac1771bdec77b5e35f415cf76acf71f407  kube-scheduler.yaml

# Getting the sha512sum of a container binary

# Get PID of kube-apiserver
$ ps -ef | grep api
root     1680878 1680807  9 Feb02 ?        1-16:53:37 kube-apiserver --advertise-address=10.154.161.198

# Go to /proc folder and find the path in container root
$ cd /proc/1680878
$ ls -al exe
lrwxrwxrwx 1 root root 0 Feb 20 21:46 exe -> /usr/local/bin/kube-apiserver
$ cd root/usr/local/bin/

# Get the sum
$ sha512sum kube-apiserver
188924764a356c959eecebb32248462b3745d86bd9f7c55bd5754b1474b901403607fedc1b6fd472cfde5d280cd3688c8620e5d5adad3ecc9f1a4856892b7da9  kube-apiserver
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
