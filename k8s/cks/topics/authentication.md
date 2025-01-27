# Authentication and Authorization

Controlling Access to the Kubernetes API:
https://kubernetes.io/docs/concepts/security/controlling-access/

API Requests are always tied to:
- Users
- ServiceAccount
- Anonymous

Every request must authenticate unless done anonymously.

Things we should restrict by default:
- Anonymous access
- Close insecure port
- Dont expose the API server externally
- Restrict Access from Nodes to API (NodeRestriction)
- Prevent unauthorized access (RBAC)
- Prevent pods from talking to the API.


Different ways you can connect:

- Outside -> API (user)
- Pod -> API (automounted tokens)
- Node -> API (kubelet)

# Disble Anonymous Access

Go to the control plane where there is the API Server manifest. Add `--anonymous-auth=false`

Then you get unauthorized:

```sh
$ curl -k https://localhost:6443
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "Unauthorized",
  "reason": "Unauthorized",
  "code": 401
}
```

# Remove the Insecure Port

Go to the control plane where there is the API Server manifest. Remove  `--insecure-port=8080`

- Sent over HTTP
- Bypasses authentication and authorization modules
- Admission Controller is still enforced

If you want to disable the insecure port, set it to 0: `--insecure-port=0`

Certificates

# User Authenticaton via curl

You can get the certificate authority and user certificate and key from the `~/.kube/config` or by doing `kube config view --raw`.

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBD0...
    server: https://10.154.161.198:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUS...
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFUR...
```

Then you echo out all of the `base64` encoded items to a file after decoding:

```sh
# Dump out the certificate authority
echo "LS0tLS1CRUdJTiBD0..." | base64 -d > ca.crt

# Dump out the Admin user certificate and key
echo "LS0tLS1CRUdJTiBDRVJUS..." | base64 -d > admin.crt
echo "LS0tLS1CRUdJTiBSU0EgUFJJVkFUR..." | base64 -d > admin.key
```

Now you can use them to get information about the cluster

```sh
$ curl https://10.154.161.198:6443 --cacert ca.crt --cert admin.crt --key admin.key
{
  "paths": [
    "/.well-known/openid-configuration",
    "/api",
    "/api/v1",
    "/apis",
    "/apis/",
    "/apis/admissionregistration.k8s.io",
    "/apis/admissionregistration.k8s.io/v1",
    "/apis/apiextensions.k8s.io",
    "/apis/apiextensions.k8s.io/v1",
    "/apis/apiregistration.k8s.io",
    "/apis/apiregistration.k8s.io/v1",
    "/apis/apps",
    "/apis/apps/v1",
    "/apis/authentication.k8s.io",
    "/apis/authentication.k8s.io/v1",
    "/apis/authorization.k8s.io",
    "/apis/authorization.k8s.io/v1",
    "/apis/autoscaling",
    "/apis/autoscaling/v1",
    "/apis/autoscaling/v2",
    "/apis/batch",
    "/apis/batch/v1",
    "/apis/certificates.k8s.io",
    "/apis/certificates.k8s.io/v1",
    "/apis/configuration.konghq.com",
    "/apis/configuration.konghq.com/v1",
    "/apis/configuration.konghq.com/v1alpha1",
    "/apis/configuration.konghq.com/v1beta1",
    "/apis/coordination.k8s.io",
    "/apis/coordination.k8s.io/v1",
    "/apis/crd.projectcalico.org",
    "/apis/crd.projectcalico.org/v1",
    "/apis/discovery.k8s.io",
    "/apis/discovery.k8s.io/v1",
    "/apis/events.k8s.io",
    "/apis/events.k8s.io/v1",
    "/apis/flowcontrol.apiserver.k8s.io",
    "/apis/flowcontrol.apiserver.k8s.io/v1",
    "/apis/flowcontrol.apiserver.k8s.io/v1beta3",
    "/apis/networking.k8s.io",
    "/apis/networking.k8s.io/v1",
    "/apis/node.k8s.io",
    "/apis/node.k8s.io/v1",
    "/apis/policy",
    "/apis/policy/v1",
    "/apis/rbac.authorization.k8s.io",
    "/apis/rbac.authorization.k8s.io/v1",
    "/apis/scheduling.k8s.io",
    "/apis/scheduling.k8s.io/v1",
    "/apis/storage.k8s.io",
    "/apis/storage.k8s.io/v1",
    "/healthz",
    "/healthz/autoregister-completion",
    "/healthz/etcd",
    "/healthz/log",
    "/healthz/ping",
    ...
    "/livez",
    "/livez/autoregister-completion",
    "/livez/etcd",
    "/livez/log",
    "/livez/ping",
    "/logs",
    "/metrics",
    "/metrics/slis",
    "/openapi/v2",
    "/openapi/v3",
    "/openapi/v3/",
    "/openid/v1/jwks",
    "/readyz/shutdown",
    "/version"
  ]
}
```

You can get the version:

```sh
$ curl https://10.154.161.198:6443/version --cacert ca.crt --cert admin.crt --key admin.key
{
  "major": "1",
  "minor": "31",
  "gitVersion": "v1.31.3",
  "gitCommit": "c83cbee114ddb732cdc06d3d1b62c9eb9220726f",
  "gitTreeState": "clean",
  "buildDate": "2024-11-19T13:48:20Z",
  "goVersion": "go1.22.8",
  "compiler": "gc",
  "platform": "linux/amd64"
}
```

# Enable Cluster Externally

All you need to do is change your Kubernetes service in the `default` namespace from ClusterIP to NodePort.

Then you can download the kubeconfig and change the service IP address to the cluster and NodePort.

You may have to put the DNS name in `/etc/hosts`.

# Addmission Controller

## NodeRestriction

To ensure workload isolation, limits the node labels that a kubelet can modify

`kube-apiserver --enable-admission-plugins=NodeRestriction`

Check status by going to `/etc/kubernetes/manifests/kube-apiserver.yaml`

Log into the worker, set the kubeconfig and you can't edit labels on the master:

```sh
export KUBECONFIG=/etc/kubernetes/kubelet.conf
$ k get nodes
NAME     STATUS   ROLES           AGE    VERSION
master   Ready    control-plane   6d1h   v1.29.6
worker   Ready    <none>          6d1h   v1.29.6

$ k edit node master
error: nodes "master" could not be patched: nodes "master" is forbidden: node "worker" is not allowed to modify node "master"
```

But you can edit the labels on the worker:

```sh
$ k edit node worker
```

Except labels that start with `node-restriction`:

```sh
$ kubectl label node worker node-restriction.kubernetes.io/test=yes
Error from server (Forbidden): nodes "worker" is forbidden: is not allowed to modify labels: node-restriction.kubernetes.io/test
```
