# ServiceAccounts and Users

There are two times of major authentication mechanisms in Kubernetes:

- ServiceAccounts
- Users

**ServiceAccounts** are used by Pods and other Kubernetes resources to limit the scope of access to resources in the cluster. For example, you may only want a pod to only be able to access resources within its own namespace. Like users, authorization is controlled by RBAC.

**Users** are used to login to the Kubernetes API and can be limited with RBAC like Roles, ClusterRoles, RoleBindings, and ClusterRoleBindings.

# Serivce Accounts

Creating a ServiceAcount is very easy in Kubernetes:

```sh
kubectl create serviceaccount nginx-sa -o yaml > nginx-sa.yaml
kubectl apply -f nginx-sa.yaml
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2023-01-11T03:48:24Z"
  name: nginx-sa
  namespace: nginx-test
  resourceVersion: "1941804"
  uid: 4db911ee-12fa-4669-a993-1df3e4c946d4
```

To do anything interesting though you have to connect the service account to:

- Role
- RoleBinding
- Pod

## Role

A Role or ClusterRole defines the APIs that can be used. Here is a Rolefor just reading pods:

```sh
kubectl create role nginx-pod-reader --verb get,list,watch --resource=pods -o yaml > nginx-pod-reader-role.yaml
kubectl apply nginx-pod-reader-role.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: "2023-01-11T03:52:48Z"
  name: nginx-pod-reader
  namespace: nginx-test
  resourceVersion: "1942146"
  uid: c0223fcd-1e6d-427a-8f8e-02ca2f72967b
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
  - watch
```

You can get the list of resources from `kubectl api-resources`. Verbs are defined as API request types

https://kubernetes.io/docs/reference/access-authn-authz/authorization/#determine-the-request-verb

- create (POST)
- get, list, watch (GET)
- update (PUT)
- patch (PATCH)
- delete, deletecollection (DELETE)

## RoleBinding

With the role created you now how to connect the role and user together:

```sh
kubectl create rolebinding nginx-role-binding --role nginx-pod-reader --serviceaccount default:nginx-sa -o yaml > nginx-role-binding.yaml
kubectl apply -f nginx-role-binding.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: nginx-role-binding
  namespace: nginx-test
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: nginx-pod-reader
subjects:
- kind: ServiceAccount
  name: nginx-sa
  namespace: default
```

You then can test powers by the following

```sh
kubectl auth can-i list pods --namespace default --as system:serviceaccount:default:nginx-sa
```


## Pod

Finally launch your pod using the serviceAccount

https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  serviceAccountName: nginx-sa
  ...
```

# Users

It is most people's K8s experience that they are given a `.kubeconfig` file that has admin access to a cluster. It is often generated directly from the K8s Admin config file (often named admin.conf). This is like giving giving `root` access to a Linux system and is generally bad practice. In the real world you don't want users of clusters to have access to the full cluster, so you limit user privilege. For bigger organizations, you'd use a third-party, custom, or managed authentication providers like Okta that use a standard interface like OpenID Connect (OIDC). 

In the following examples, I will assume a smaller cluster where you have to manually control the user access.

1. Generate a private key and a Certificate Signing Request (CSR). Note that the name (`/CN`) and group (`/O`) are passed to the CSR

```sh
openssl genrsa -out emartin.key 2048
openssl req -new -key emartin.key -out emartin.csr -subj "/CN=emartin/O=devops"
```

Next you must take the CSR and pass it in the `request:` field of a Kubernetes CertificateSigningRequest manifest. The CSR must be Base64 encoded into the manifest

```sh
cat <<EOF > emartin.yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: emartin
spec:
  signerName: kubernetes.io/kube-apiserver-client
  groups:
  - system:authenticated
  request: $(cat emartin.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - client auth
EOF
```

Now apply the user yaml file generated:

```sh
kubectl apply -f emartin.yaml
```

Once applied, the CSR goes into a Pending status:

```sh
$ kubectl get csr              
NAME      AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
emartin   45s   kubernetes.io/kube-apiserver-client   kubernetes-admin   <none>              Pending
```

You have to manually approve the certificate process, 

```sh
kubectl certificate approve emartin
```

The CSR will be in an Approved/Issued state:

```sh
$ kubectl get csr                    
NAME      AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
emartin   75s   kubernetes.io/kube-apiserver-client   kubernetes-admin   <none>              Approved,Issued
```

Once approved you can retrieve the certificate from the `certificate:` field in the `status:` section of the manifest:

```sh
kubectl get csr emartin -o jsonpath='{.status.certificate}' | base64 -d > emartin.crt
```

You should now have a `emartin.key`, `emartin.crt`.  If you have access to the CA crt on the master you can take a shortcut a create the key and certificate all from the command-line:

```sh
# Generate the private key
openssl genrsa -out emartin.key 2048

# Generate the CSR
openssl req -new -key emartin.key -out emartin.csr -subj "/CN=emartin@internal.users/O=devops"

# With the CSR and the CA from the server create the crt
openssl x509 -req -in emartin.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out emartin.crt -days 500
```

These are not useful until you "bind" it to either a Role or a ClusterRole through a RoleBinding or ClusterRoleBinding, respectively. Roles are namespaced scopes, while ClusterRoles apply to the entire cluster. But you can at least create the kubeconfig:

```sh
# Set the config credentials using the key and the crt
kubectl config set-credentials emartin@internal.users --client-key=emartin.key --client-certificate=emartin.crt
kubectl config set-context emartin@internal.users --cluster=kubernetes --user=emartin@internal.users
```

The next section is about user binding.

# User Binding

In the examples above, the user the user creation isn't complete from the cluster perspective. For example, if you want to make the new user a Cluster Admin, you simply create a role binding that binds the `devops` Group to the `cluster-admin` role like so:

```sh
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: devops
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: devops
EOF
```

To generate the `.kubeconfig`, you need two more things:

- The Kubernetes API server for the cluster (eg. k8s-master)
- The Certificate Authority certificat (ca.crt)

You can get the API server from an existing `.kubeconfig`. Use `scp` or some other tool to get the certificate authority key like so:

```sh
scp k8s-master:/etc/kubernetes/pki/ca.crt ./ca.crt
```

```sh
KUBECONFIG=emartin.kubeconfig kubectl config set-cluster devops-cluster --server=https://k8s-master:6443 --certificate-authority=ca.crt --embed-certs=true
KUBECONFIG=emartin.kubeconfig kubectl config set-credentials emartin --client-certificate=emartin.crt --client-key=emartin.key --embed-certs=true
KUBECONFIG=emartin.kubeconfig kubectl config set-context devops --cluster=devops-cluster --namespace=default --user=emartin
KUBECONFIG=emartin.kubeconfig kubectl config use-context devops
```

Helpful pages:
- https://gist.github.com/etiennetremel/c2555e3c8a8b25c780c1b506fadf2aa2
- https://gist.github.com/tony612/2e29f3d7b137db724db97b817bcadce8
