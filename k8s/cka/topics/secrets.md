# Secrets

Secrets are very similar to [ConfigMaps](./configmaps.md). Like ConfigMaps, they store their data in a `data:` map within the manifest. They are sometimes tricky to deal with because of the different types and how you interact with them in pods and service accounts.

https://kubernetes.io/docs/concepts/configuration/secret/

There are multiple secret types that are used in Kubernetes (manifest `type:` values are specified in parenthesis):

- Generic or Opaque - arbitrary user-defined data (`Opaque`)
-	ServiceAccount token (`kubernetes.io/service-account-token`)
- Serialized ~/.dockercfg file for `imagePullSecrets` (`kubernetes.io/dockercfg`)
- Serialized ~/.docker/config.json file for `imagePullSecrets` (`kubernetes.io/dockerconfigjson`)
- Credentials for basic authentication (`kubernetes.io/basic-auth`)
- Credentials for SSH authentication (`kubernetes.io/ssh-auth`)
- Data for a TLS client or server (`kubernetes.io/tls`)
- Bootstrap token data (`bootstrap.kubernetes.io/token`)

Get a list of all secrets in your cluster by type:

```sh
$ kubectl get secrets -A -o=custom-columns="NAME:.metadata.name,NAMESPACE:.metadata.namespace,TYPE:.type"
NAME                              NAMESPACE              TYPE
nginx-secret                      default                Opaque
nginx-secret-file                 nginx-test             Opaque
nginx-secret-sa                   nginx-test             kubernetes.io/service-account-token
nginx-secret-stringdata           nginx-test             Opaque
nginx-tls-secret                  nginx-test             kubernetes.io/tls
```

# Encoding Secrets with Base64

It is usually best practice to encode secrets using [Base64](https://en.wikipedia.org/wiki/Base64) encoding, but it is not a requirement in the source manifest. This encoding is **not** encryption so can be easily determined through an admin `kubectl` command.  

In a manifest you specify one or both fields to specify the secret data:

- `data:` - encoded values
- `stringData:` - unencoded values

For example:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-secret-stringdata
data:
  KEY1: MTIzNA==
  KEY2: MTIzNA==
  KEY3: MTIzNCA1Njc4
stringData:
  KEY1_UNENCODED: "1234"
  KEY2_UNENCODED: "1234"
  KEY3_UNENCODED: "1234 5678"
```

Note though that the `stringData:` key/values will be transformed into `data:` key/values in the created secret:

```yaml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: nginx-secret-stringdata
  namespace: nginx-test
data:
  KEY1: MTIzNA==
  KEY1_UNENCODED: MTIzNA==
  KEY2: MTIzNA==
  KEY2_UNENCODED: MTIzNA==
  KEY3: MTIzNCA1Njc4
  KEY3_UNENCODED: MTIzNCA1Njc4
```

You can decrypt any value in the `data:` map with `base64 -d`:

```sh
$ echo "MTIzNA==" | base64 -d
1234
```

You can encode a value with `base64`:

```sh
$ echo -n "1234" | base64
MTIzNA==
```

Note that the `-n` is needed when encoding so that the implicit newline (eg. `"1234\n"`) won't be encoded with the secret

Secrets can also be marked in the manifest as `immutable: false` which would require the secret to be destroyed and re-created.

# Generic Secret

Generic secrets are the most common way to store secrets. They are also know as Opaque secrets because the `type:` field get set to `Opaque` in the manifest.

## Generic Secret Creation

There are two ways that you can create them from the command line that is most convenient:

- Literals
- Files

### Create with --from-literal

A Literal you just pass on the command-line as a string literal and it will be visible in the shell history:

```sh
kubectl create secret generic nginx-secret --from-literal=KEY1=1234
```

Multiple literals can also be specified:

```sh
kubectl create secret generic nginx-secret --from-literal KEY1=1234 --from-literal KEY2=1234 --from-literal "KEY3=1234 5678"
```

Notice the Following:

- Like most of `kubectl` usage, `--from-literals` does not require a `=` before the key value pairs for the secrets.
- If a secret needs a space, wrap it in double quotes
- Secrets are stored in the `data:` section in the manifest
- Secrets are obfuscated via `base64` encoding, not encrypted

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-secret
data:
  KEY1: MTIzNA==
  KEY2: MTIzNA==
  KEY3: MTIzNCA1Njc4
```

### Create with --from-file

Creating a secret from a file encodes the entire file using the filename as the key. First create the secret files:

```sh
echo -n "1234" > KEY1
echo -n "1234" > KEY2
echo -n "1234 5678" > KEY3
```

Then create the secret:

```sh
kubectl create secret generic nginx-secret-file --from-file ./KEY1 --from-file ./KEY2 --from-file ./KEY3
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-secret-file
data:
  KEY1: MTIzNA==
  KEY2: MTIzNA==
  KEY3: MTIzNCA1Njc4
```

Notice the secret that is created is the same as above that was created by literals

## Attaching Secrets to a Pod

There are three common ways of attaching a secret to a pod for usage:

- Volume Mounting
- Loading all secret keys into environment
- Loading a single secret key into the environment

### Volume Mounting

The secret is already created from above and it simply is mounted into a folder path `/secret` in the pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-secret-volume-mount
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-secret-volume
      mountPath: "/secret"
      readOnly: true
  volumes:
  - name: nginx-secret-volume
    secret:
      secretName: nginx-secret-file
```

Each of the keys will be files on the file system:

```sh
$ kubectl exec nginx-secret-volume-mount -it -- ls -l /secret 
total 0
lrwxrwxrwx 1 root root 11 Jan  8 19:49 KEY1 -> ..data/KEY1
lrwxrwxrwx 1 root root 11 Jan  8 19:49 KEY2 -> ..data/KEY2
lrwxrwxrwx 1 root root 11 Jan  8 19:49 KEY3 -> ..data/KEY3
```

And the contents of the file will be the unencoded values:

```sh
$ kubectl exec nginx-secret-volume-mount -it -- sh -c "cat /secret/KEY1"
1234

$ kubectl exec nginx-secret-volume-mount -it -- sh -c "cat /secret/KEY3"
1234 5678
```

### Loading All Secret Keys into Environment

This is probably the easiest to load, directly into the environment:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-secret-env-from
spec:
  containers:
    - name: nginx
      image: nginx
      envFrom:
      - secretRef:
          name: nginx-secret-file
```

And then you can get all of the keys from the environment

```sh
$ kubectl exec nginx-secret-env-from -it -- sh -c "env | grep KEY"
KEY1=1234
KEY2=1234
KEY3=1234 5678
```

### Loading a Single Secret Key into Environment

This is the most tedious way to load an item as it requires 5 lines to only pull a single key from a secret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-secret-single-env
spec:
  containers:
    - name: nginx
      image: nginx
      env:
        - name: KEY1
          valueFrom:
            secretKeyRef:
              name: nginx-secret-file
              key: KEY1
```

And then you can get the key from the environment:

```sh
$ kubectl exec nginx-secret-single-env -it -- sh -c "env | grep KEY"
KEY1=1234
```

# Service Account Token

Starting in K8s 1.24 the TokenRequest API is supposed to be used rather than manually creating tokens. That is done using the following

```sh
$ kubectl create token nginx-sa --duration 10m
eyJhbGciO...
```

However, sometimes you don't want to use this mechanism. Service accounts can have hardcoded secrets. Service account tokens have a secret `type:` of `kubernetes.io/service-account-token` in the manifest. First create the service account user name:

```sh
kubectl create sa nginx-sa
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-sa
```

And then manually create a secret where you don't need to fill in the `token` field:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-secret-sa
  annotations:
    kubernetes.io/service-account.name: "nginx-sa"
type: kubernetes.io/service-account-token
data: {}
```

Kubernetes will manually set the `ca.crt` and `token` key/values:

```yaml
apiVersion: v1
kind: Secret
data:
  ca.crt: LS0tLS...
  token: ZXlKaGJHY2...
metadata:
  annotations:
    kubernetes.io/service-account.name: nginx-sa
    kubernetes.io/service-account.uid: a7ac55a1-cdde-4360-a65a-8ecb20dc5529
  creationTimestamp: "2023-01-08T20:19:00Z"
  name: nginx-secret-sa
  namespace: nginx-test
  resourceVersion: "1684029"
  uid: 7c91e923-8b71-478c-95b2-9c365e869883
type: kubernetes.io/service-account-token
```

# Docker Registry Secret

You can create a docker registry secret that can be used to access a remote Docker registry for working with images. They are often used with `imagePullSecrets` within Pod definitions. Here is how to create the secret:

```sh
$ kubectl create secret docker-registry docker-registry-secret \
  --docker-email=registryuser@example.com \
  --docker-username=registryuser \
  --docker-password=1234 \
  --docker-server=my-registry.example.com:5000
```

The `data:` is stored in a `.dockerconfigjson` key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: docker-registry-secret
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: eyJhdXRocyI6eyJteS1yZWdpc3RyeS5leGFtcGxlLmNvbTo1MDAwIjp7InVzZXJuYW1lIjoicmVnaXN0cnl1c2VyIiwicGFzc3dvcmQiOiIxMjM0IiwiZW1haWwiOiJyZWdpc3RyeXVzZXJAZXhhbXBsZS5jb20iLCJhdXRoIjoiY21WbmFYTjBjbmwxYzJWeU9qRXlNelE9In19fQ==
```

Which decodes to:

```sh
$ echo "eyJhdXRocyI6eyJteS1yZ..." | base64 -d | jq .
{
  "auths": {
    "my-registry.example.com:5000": {
      "username": "registryuser",
      "password": "1234",
      "email": "registryuser@example.com",
      "auth": "cmVnaXN0cnl1c2VyOjEyMzQ="
    }
  }
}
```

Notice the type in the secret manifest is `kubernetes.io/dockerconfigjson`.

To specify an imagePullSecret in a Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-image-pull-secret
spec:
  containers:
    - name: nginx
      image: nginx
  imagePullSecrets:
    - name: docker-registry-secret
```

You can also specify an `imagePullSecret` at the service account level:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2023-01-08T18:51:52Z"
  name: nginx-sa
  namespace: nginx-test
  resourceVersion: "1677217"
  uid: a7ac55a1-cdde-4360-a65a-8ecb20dc5529
imagePullSecrets:
  - name: docker-registry-secret
```

This is **very** useful if you don't want to specify an imagePullSecret for each pod you want to start.

# Basic Auth

The Kubernetes documentation is excellent for defining basic auth secrets so I will copy straight from there:

https://kubernetes.io/docs/concepts/configuration/secret/#basic-authentication-secret

>The `kubernetes.io/basic-auth` type is provided for storing credentials needed for basic authentication. When using this `Secret` type, the data field of the Secret must contain one of the following two keys:
>
- username: the user name for authentication
- password: the password or token for authentication

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-secret-basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: admin      # required field
  password: t0p-Secret # required field
```

>The basic authentication Secret type is provided only for convenience. You can create an Opaque type for credentials used for basic authentication. However, using the defined and public Secret type (kubernetes.io/basic-auth) helps other people to understand the purpose of your Secret, and sets a convention for what key names to expect. The Kubernetes API verifies that the required keys are set for a Secret of this type.

# TLS Secrets

TLS Secrets are used to promote SSL/TLS for things like Ingress. The secret requires two files:

- tls.crt - public key certificate
- tls.key - private key

Create the keys:

```sh
# Create private key
openssl genrsa -out tls.key 2048

# Create public cert
openssl req -x509 -new -nodes -days 365 -key tls.key -out tls.crt -subj "/CN=example.com"

# Create the secret
kubectl create secret tls nginx-tls-secret --cert=./tls.crt --key=./tls.key
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-tls-secret
  namespace: nginx-test
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRU...
  tls.key: LS0tLS1CRUdJ...
```

# Bootstrap token secrets

Another secret that you don't have to use that often except to setup a new node in the cluster. The documentation is again great.

https://kubernetes.io/docs/concepts/configuration/secret/#bootstrap-token-secrets

>A bootstrap token Secret can be created by explicitly specifying the Secret type to bootstrap.kubernetes.io/token. This type of Secret is designed for tokens used during the node bootstrap process. It stores tokens used to sign well-known ConfigMaps.
>
>A bootstrap token Secret is usually created in the kube-system namespace and named in the form bootstrap-token-<token-id> where <token-id> is a 6 character string of the token ID.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: bootstrap-token-5emitj
  namespace: kube-system
type: bootstrap.kubernetes.io/token
data:
  auth-extra-groups: c3lzdGVtOmJvb3RzdHJhcHBlcnM6a3ViZWFkbTpkZWZhdWx0LW5vZGUtdG9rZW4=
  expiration: MjAyMC0wOS0xM1QwNDozOToxMFo=
  token-id: NWVtaXRq
  token-secret: a3E0Z2lodnN6emduMXAwcg==
  usage-bootstrap-authentication: dHJ1ZQ==
  usage-bootstrap-signing: dHJ1ZQ==
```  

>A bootstrap type Secret has the following keys specified under data:

- `token-id`: A random 6 character string as the token identifier. Required.
- `token-secret`: A random 16 character string as the actual token secret. Required.
- `description`: A human-readable string that describes what the token is used for. Optional.
- `expiration`: An absolute UTC time using RFC3339 specifying when the token should be expired. Optional.
- `usage-bootstrap-<usage>`: A boolean flag indicating additional usage for the bootstrap token.
- `auth-extra-groups`: A comma-separated list of group names that will be authenticated as in addition to the system:bootstrappers group.
