# Kubernetes Tools

Useful tools to install for managing and maintaining Kubernetes:

- [Kubernetes Lens](https://k8slens.dev)
- [K9s](https://k9scli.io)
- [Kubernetes Dashboard](https://github.com/kubernetes/dashboard)
- [kubens/kubectx](https://github.com/ahmetb/kubectx)

# K9s

Install on Mac:

```sh
brew install derailed/k9s/k9s
```

# Kubernetes Dashboard

Apply the dashboard from Github (check tags for releases):

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

Apply the dashboard user and cluster role binding:

https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dashboard-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: dashboard-user
  namespace: kubernetes-dashboard
```

Generate the token for the dashboard user:

```sh
$ kubectl -n kubernetes-dashboard create token dashboard-user
eyJhbGciOiJSU...
```

Open up the port (for external access) then port forward to the service

```sh
sudo ufw allow 39447
kubectl port-forward svc/kubernetes-dashboard -n kubernetes-dashboard --address 0.0.0.0 39447:443
```

Cut and paste the token into the login screen and you are in.

# kubectx / kubens

Install kubectx/kubens on Mac

```sh
brew install kubectx
```

Install kubectx/kubens on Linux

```sh
sudo apt install kubectx

or

sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
```