# Service Accounts

Service Accounts are used by pods and deployments for access to the Kubernetes API.

Service Accounts
- Namespaced
- Default service account in every namespace used by Pods
- Used to talk to the Kubernetes API.
- Always has a secret (token)

# Example Scenario

Create ServiceAccount and use in Pod. Use ServiceAccount token to connect to the API from inside the Pod

List all ServiceAccounts

```sh
$ kubectl get sa
NAME      SECRETS   AGE
default   0         7d
```

Create a new service account

```sh
$ kubectl create sa accessor
serviceaccount/accessor created

$ kubectl get sa
NAME       SECRETS   AGE
accessor   0         27s
default    0         7d
```

Get the token of the new service account:

```sh
$ kubectl create token accessor
eyJhbGciOiJSUzI1...
```

You can take that token which is a JWT token and inspect it at https://jwt.io

And you can see the payload:

```json
{
  "aud": [
    "https://kubernetes.default.svc.cluster.local"
  ],
  "exp": 1737949288,
  "iat": 1737945688,
  "iss": "https://kubernetes.default.svc.cluster.local",
  "jti": "a255c024-b7db-485c-823e-0110ff2b5228",
  "kubernetes.io": {
    "namespace": "default",
    "serviceaccount": {
      "name": "accessor",
      "uid": "e344807e-a89f-4fdf-82bb-d6af04f91ca2"
    }
  },
  "nbf": 1737945688,
  "sub": "system:serviceaccount:default:accessor"
}
```

Pods have access to the service account if it is used. Create a pod:

```sh
$ k run accessor --image=nginx --dry-run=client -oyaml > nginx.yaml
```

Add a serviceAccountName that doesn't exist:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: accessor
  name: accessor
spec:
  serviceAccountName: test
  containers:
  - image: nginx
    name: accessor
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

You get an error that the service account doesn't exist:

```sh
$ k apply -f pod.yaml
Error from server (Forbidden): error when creating "pod.yaml": pods "accessor" is forbidden: error looking up service account default/test: serviceaccount "test" not found
```

Change serviceAccountName to `accessor` and it will apply:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: accessor
  name: accessor
spec:
  serviceAccountName: accessor
  containers:
  - image: nginx
    name: accessor
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Now if we exec into the pod

```sh
$ k exec accessor -it -- bash
root@accessor:/#
```

Kubernetes mounts the token into the pod:

```sh
root@accessor:/# mount | grep ser
tmpfs on /run/secrets/kubernetes.io/serviceaccount type tmpfs (ro,relatime,size=3905800k)
```

You can see what is affiliated with that service account:

```sh
# CA Cert, namespace, and token
root@accessor:/# ls /run/secrets/kubernetes.io/serviceaccount
ca.crt  namespace  token

# Token
root@accessor:/# cat /run/secrets/kubernetes.io/serviceaccount/token
eyJhbGciOiJSUzI1NiIsImtpZCI6ImsyNVc0YVItazNfTUtFNlRoVUdPenZBYVdIejZETnVvTkoxQjcyVGgwbXcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNzY5NDgyMTI1LCJpYXQiOjE3Mzc5NDYxMjUsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwianRpIjoiNzk4YTE2YmQtY
```

Tools inside the pod can communicate with the Kubernetes API. Get the list of the environment variables:

```sh
root@accessor:/# env | grep KUBE
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT_443_TCP=tcp://10.246.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_ADDR=10.246.0.1
KUBERNETES_SERVICE_HOST=10.246.0.1
KUBERNETES_PORT=tcp://10.246.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
```

You can `curl` the Kubernetes Host but it will be anonymous:

```sh
root@accessor:/# curl -k https://10.246.0.1
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {},
  "code": 403
}
```

You can pass the token to the `Authorization` header like so:

```sh
root@accessor:/# curl -k https://10.246.0.1 H "Authorization: Bearer eyJhbGciOiJSUzI1N..."
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "forbidden: User \"system:serviceaccount:default:accessor\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {},
  "code": 403
}
```

Notice it says forbidden for the accessor service account. Let's give that token some access.

# Disable the automount of Service Account token

You can do it by ServiceAccount:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: accessor
  namespace: default
automountServiceAccountToken: false
```

or Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: accessor
  name: accessor
spec:
  serviceAccountName: accessor
  automountServiceAccountToken: false
  containers:
  - image: nginx
    name: accessor
...
```

Once re-applied, you can't see the token mounted AND no volumes in the pod definition.

Reset the automount to `true` for the next session.

# Give the ServiceAccount Access

You want to give the pod "edit" access to the cluster. Create a ClusterRoleBinding for the ClusterRole "edit":

```sh
$ kubectl create clusterrolebinding accessor --clusterrole=edit --serviceaccount "default:accessor"
clusterrolebinding.rbac.authorization.k8s.io/accessor created
```

And then the ServiceAccount can do stuff:

```sh
$ kubectl auth can-i delete secrets --as system:serviceaccount:default:accessor
yes
```
