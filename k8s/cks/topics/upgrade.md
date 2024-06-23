# Upgrading Kubernetes

Upgrading kubeadm clusters
https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

Major.minor.patch (1.27.6)

Minor version every 3 months

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
$ apt-cache show kubeadm | grep Version
Version: 1.29.6-1.1
Version: 1.29.5-1.1
Version: 1.29.4-2.1
Version: 1.29.3-1.1
Version: 1.29.2-1.1
Version: 1.29.1-1.1
Version: 1.29.0-1.1
Version: 1.28.11-1.1
Version: 1.28.10-1.1
Version: 1.28.9-2.1
Version: 1.28.8-1.1
Version: 1.28.7-1.1
Version: 1.28.6-1.1
Version: 1.28.5-1.1
Version: 1.28.4-1.1
Version: 1.28.3-1.1
Version: 1.28.2-1.1
Version: 1.28.1-1.1
Version: 1.28.0-1.1
Version: 1.27.15-1.1
Version: 1.27.14-1.1
Version: 1.27.13-2.1
Version: 1.27.12-1.1
Version: 1.27.11-1.1
Version: 1.27.10-1.1
Version: 1.27.9-1.1
Version: 1.27.8-1.1
Version: 1.27.7-1.1
Version: 1.27.6-1.1
Version: 1.27.5-1.1
Version: 1.27.4-1.1
Version: 1.27.3-1.1
Version: 1.27.2-1.1
Version: 1.27.1-1.1
Version: 1.27.0-2.1
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

