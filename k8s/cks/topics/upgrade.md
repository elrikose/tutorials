# Upgrading Kubernetes

Upgrading kubeadm clusters
https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

Major.minor.patch (1.27.6)

Minor version every 3 months

Why do you upgrade?
- Support
- Security Fixes
- Bug Fixes
- Stay Up to Date for Dependencies

# Upgrade Mechanism

- Upgraded Control Plane components (apiserver, scheduler, etc)
- Upgrade Worker Nodes (kubelet, kube-proxy)
- Components should be on the same minor version or one below apiserver
- Kubelet can be two minor versions under, but shouldn't

# How to Upgrade

- `kubectl drain`
- Upgrade master
- Upgrade worker
- `kubectl uncordon`

Drain the master node:

```sh
kubectl drain master --ignore-daemonsets
```

On Ubuntu, show what versions you can upgrade to:

```sh
$ sudo apt get update
$ sudo apt-cache show kubeadm | grep Version
Version: 1.32.6-1.1
Version: 1.32.5-1.1
Version: 1.32.4-1.1
Version: 1.32.3-1.1
Version: 1.32.2-1.1
Version: 1.32.1-1.1
Version: 1.32.0-1.1
Version: 1.31.10-1.1
Version: 1.31.9-1.1
Version: 1.31.8-1.1
Version: 1.31.7-1.1
Version: 1.31.6-1.1
Version: 1.31.5-1.1
Version: 1.31.4-1.1
Version: 1.31.3-1.1
Version: 1.31.2-1.1
Version: 1.31.1-1.1
Version: 1.31.0-1.1
```

Unmark kubeadm for upgrade:

```sh
apt-mark unhold kubeadm
```

Upgrade control plane:

```sh
sudo apt install kubeadm=1.29.6-1.1
```

```sh
kubectl upgrade plan
kubectl upgrade apply v1.29.6
```

Now upgrade the kubectl and kubelet:

```sh
sudo apt install kubectl=1.29.6-1.1 kubelet=1.29.6-11
sudo systemctl restart kubelet
```

Drain the worker node

```sh
kubectl drain worker
```

SSH into worker

```sh
sudo apt install kubeadm=1.29.6-1.1
sudo kubeadm upgrade node
```
Then upgrade the kubectl and kubelet:

```sh
sudo apt install kubectl=1.29.6-1.1 kubelet=1.29.6-11
```

```sh
kubectl uncordon worker
```
