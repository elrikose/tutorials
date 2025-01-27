# Role-based Access Control (RBAC)

Role-based Access Control is configured in the `kube-apiserver` via `--authorization-mode=RBAC`. The default is `AlwaysAllow`, but you can also add `Node` like `--authorization-mode=Node`.

RBAC
- Restrict access to Kubernetes resources when accessed by either Users or Service Accounts
- Works with Roles and Bindings
- Whitelist what is allowed, everything else is denied
- Principle of Least Privileged

# Namespaced and Non-namespaced Resources

Namespaced resources are things like pods or deployments.

Non-namespaced resources are nodes or persistent volumes.

```sh
# Print namespaced resources
kubectl api-resources --namespaced=true

# Print non-namespaced resources
kubectl api-resources --namespaced=false
```

Roles and ClusterRole
- Define a set of permissions
  - can edit pods
  - can read secrets
- Role - One namespace
- ClusterRole - All namespaces or non-namespaced resoures

RoleBinding and ClusterRoleBinding
- Bind a role to a user or service account
- RoleBinding - Applied only in one namespace
- ClusterRoleBinding - All namespaces or non-namespaced resoures

Be careful with both ClusterRole and ClusterRoleBinding. All current and future resources will be accessible across namespaces.

Valid combinations
- Role + RoleBinding
- ClusterRole + ClusterRoleBinding
- ClusterRole + RoleBinding

Not Valid
- Role + ClusterRoleBinding - A single role can't have a binding across cluster.

Permissions are additive
- If two roles have permissions that overlap, all the non-overlapping permissions still apply

# Example Scenario - Role/RoleBinding

- Two namespaces `red` and `blue`
- User `jane` can only get secrets in namespace `red`.
- User `jane` can only get and list secrets in namespace `blue`.

Create role for namespace red:

```sh
$ kubectl create role secrets-manager --namespace red  --verb=get --verb=get --resource=secrets --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: null
  name: secrets-manager
  namespace: red
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get
```

Create role for namespace blue:

```sh
$ kubectl create role secrets-manager --namespace blue  --verb=get,list --resource=secrets --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: null
  name: secrets-manager
  namespace: blue
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get
  - list
```

Create role binding for `red`:

```sh
$ kubectl create rolebinding secrets-manager -n red --role=secrets-manager --user=jane --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: secrets-manager
  namespace: red
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secrets-manager
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jane
```

Create role binding for `blue`:

```sh
$ kubectl create rolebinding secrets-manager -n blue --role=secrets-manager --user=jane --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: secrets-manager
  namespace: blue
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secrets-manager
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jane
```

Apply all of the roles and role bindings. Then test them:

```sh
# Red Namespace
$ kubectl auth can-i -n red get secrets --as jane
yes
$ kubectl auth can-i -n red get secrets --as bob
no
$ kubectl auth can-i -n red list secrets --as jane
no

# Blue namespace
$ kubectl auth can-i -n blue get secrets --as jane
yes
$ kubectl auth can-i -n blue delete secrets --as jane
no
$ kubectl auth can-i -n blue list secrets --as jane
yes
```

# Example Scenario - ClusterRole/ClusterRoleBinding

- Create a ClusterRole deploy-delete which allows delete of deployments
- User jane can delete deployments in all namespaces
- User jim can delete deployments only in namespace red


Create the cluster role:

```sh
$ kubectl create clusterrole deploy-deleter  --verb=delete --resource=deploy --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  creationTimestamp: null
  name: deploy-deleter
rules:
- apiGroups:
  - apps
  resources:
  - deployments
  verbs:
  - delete
```

Create a ClusterRoleBinding for Jane:

```sh
$ kubectl create clusterrolebinding deploy-deleter --clusterrole=deploy-deleter --user=jane --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  creationTimestamp: null
  name: deploy-deleter
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: deploy-deleter
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jane
```

Create a RoleBinding for Bob:

```sh
kubectl create rolebinding deploy-deleter -n red --clusterrole=deploy-deleter --user=bob --dry-run=client -oyaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: deploy-deleter
  namespace: red
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: deploy-deleter
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: bob
```

Test with `kubectl auth can-i`:

```sh
# Red Namespace
$ kubectl auth can-i -n red delete deploy --as jane
yes
$ kubectl auth can-i -n red delete deploy --as bob
yes
$ kubectl auth can-i -n red list secrets --as bob
no

# Blue namespace
$ kubectl auth can-i -n blue delete deploy --as jane
yes
$ kubectl auth can-i -n blue delete deploy --as bob
no
$ kubectl auth can-i -n blue list secrets --as jane
no
```

# Users versus ServiceAccounts

ServiceAccounts
- Used by the Kubernetes API to do actions. Cluster resources

Users
- There is not resource, just an object that has a cert/key.
- The cert has to be signed by the clusters client  certificate authority (CA)
- Username is under common name /CN=jane

External providers like AWS and Google can just generate certificates and then use identity providers to do authorization.

## Flow to Generate Certs

- Using `openssl` a Certificate Signing Request (CSR) is created.
- The CSR is embedded into the Kubernetes `CertificateSigningRequest`.
- The CertificateSigningRequest is accepted and the cert is returned in the request


- There is no way to invalidate a certificate! Except the expiration date.
- How to fix if a certificate is captured:
  - Create a new CA
  - Remove all access for that user in RBAC
  - Username cannot be used until cert is expired

# Creating a user

- Create a Certificate/Key for user Jane
- Sign CSR using Kubernetes API
- Use certificate/key to connect to Kubernetes API

Create a Certificate and Key:

```sh
$ openssl genrsa -out jane.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
.....+++++
.+++++
e is 65537 (0x010001)
```

Create a CSR setting the Common Name to Jane

```sh
$ openssl req -new -key jane.key -out jane.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:jane
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:

$ ls jane*
jane.csr  jane.key
```

Get the CertificateSigningRequest from the Kubernetes documentation:

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: jane
spec:
  request: ...
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - client auth
```

Replace the `request:` line with the base64 encoding:

```sh
$ cat jane.csr | base64 | tr -d "\n"
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS...
```

Apply the CSR and then approve it:

```sh
kubectl certificate approve jane
```

And then get the certificate out of the request:

```sh
$ kubectl get csr jane -o jsonpath='{.status.certificate}'| base64 -d > jane.crt
```

And then you create a user via `kubectl config`

```sh
kubectl config set-credentials jame --client-key=jane.key --client-certificate=jane.crt
```

Or you can embed the actual files:

```sh
kubectl config set-credentials jame --client-key=jane.key --client-certificate=jane.crt --embed-certs
```

List the Raw un-redacted values of the certs:

```sh
kubectl config view --raw
```

Then you have to set and use the contexts:

```sh
kubectl config set-context jane --user=jane --cluster=kubernetes
kubectl config use-context jane
```
