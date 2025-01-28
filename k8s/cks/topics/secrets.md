# Kubernetes Secrets

Secrets can be:

- Passwords
- API Keys
- Certificates
- Database Connection Strings
- General info needed by application

# Creating a Secret

```sh
$ kubectl create secret generic username --from-literal user=elrikose
secret/username created

$ kubectl create secret generic password --from-literal password=password
secret/password created
```

Now create a pod

```sh
kubectl run secret-pod --image nginx -oyaml --dry-run=client > secret-pod.yaml
```

```sh
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-pod
  name: secret-pod
spec:
  containers:
  - image: nginx
    name: secret-pod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

# Accessing a secret with volume

Mount a secret as a volume:

```sh
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-pod
  name: secret-pod
spec:
  volumes:
    - name: username-volume
      secret:
        secretName: username
    - name: password-volume
      secret:
        secretName: password
  containers:
  - image: nginx
    name: secret-pod-with-volume
    resources: {}
    volumeMounts:
      - name: username-volume
        readOnly: true
        mountPath: "/etc/username-volume"
      - name: password-volume
        readOnly: true
        mountPath: "/etc/password-volume"
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

and then exec into the pod and get the secrets

```sh
kubectl exec secret-pod-with-volume -it -- bash

cat /etc/username-volume/user
cat /etc/password-volume/password
```

# Accessing a secret with environment


Add an environment variable

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-pod-with-env
  name: secret-pod-with-env
spec:
  containers:
  - image: nginx
    name: secret-pod-with-env
    resources: {}
    env:
     - name: USERNAME
       valueFrom:
         secretKeyRef:
           name: username
           key: user
     - name: PASSWORD
       valueFrom:
         secretKeyRef:
           name: password
           key: password
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

```

Printing it out

```sh
$ kubectl exec secret-pod-with-env -it -- bash
root@secret-pod-with-env:/# env
...
USERNAME=elrikose
...
PASSWORD=password
```

# Accessing Secret from Worker Node

Log into the worker node and get the running containers

```sh
$ sudo crictl ps
CONTAINER           IMAGE               CREATED             STATE               NAME                                   ATTEMPT             POD ID              POD
2a997918d8ae0       e0c9858e10ed8       5 minutes ago       Running             secret-pod-with-volume                 0                   95540a92be17b       secret-pod-with-env
1fa1db01bcf1a       e0c9858e10ed8       11 minutes ago      Running             secret-pod-with-volume                 0                   c3ca29b4d3a3b       secret-pod-with-volume
```

Inspect the envionment pod and you can get it from the environment:

```sh
$ crictl inspect 2a997918d8ae0
...
        "env": [
          ...
          "USERNAME=elrikose",
          "PASSWORD=password",
          ...
        ],
```

You can also get it from the volume by getting the PID and the volume

```sh
$ sudo crictl inspect 1fa1db01bcf1a
  "info": {
    "sandboxID": "c3ca29b4d3a3b5be3fa09f5c0161916553cd57a11dee0f6942d7f0d4102a7496",
    "pid": 36524,
...
    "mounts": [
      {
        "containerPath": "/etc/username-volume",
        "gidMappings": [],
        "hostPath": "/var/lib/kubelet/pods/7cfab9f8-1b36-4788-a08d-24466f34e1f5/volumes/kubernetes.io~secret/username-volume",
        "propagation": "PROPAGATION_PRIVATE",
        "readonly": true,
        "selinuxRelabel": false,
        "uidMappings": []
      },
      {
        "containerPath": "/etc/password-volume",
        "gidMappings": [],
        "hostPath": "/var/lib/kubelet/pods/7cfab9f8-1b36-4788-a08d-24466f34e1f5/volumes/kubernetes.io~secret/password-volume",
        "propagation": "PROPAGATION_PRIVATE",
        "readonly": true,
        "selinuxRelabel": false,
        "uidMappings": []
      },
```

Confirm that it is `nginx`:

```sh
$ ps -ef | grep 36524
root       36524   36451  0 17:52 ?        00:00:00 nginx: master process nginx -g daemon off;
```

And then using the `/proc` folder you can find the secrets via being a root user

```sh
$ cd /proc/36524/root/etc/username-volume/
$ ls -l
total 0
lrwxrwxrwx 1 root root 11 Jun 22 17:52 user -> ..data/user
```

# Accessing Secret from etcd

Login to the master node as root and get the certs the API server uses for ETCD

```sh
grep etcd /etc/kubernetes/manifests/kube-apiserver.yaml
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
```

Then use the `etcdctl` command to test to see if we have access:

```sh
$ ETCDCTL_API=3 etcdctl  --cert /etc/kubernetes/pki/apiserver-etcd-client.crt --key /etc/kubernetes/pki/apiserver-etcd-client.key --cacert /etc/kubernetes/pki/etcd/ca.crt endpoint health
127.0.0.1:2379 is healthy: successfully committed proposal: took = 10.458282ms
```

And then you can get it using the `get` option

```sh
$ ETCDCTL_API=3 etcdctl --cert /etc/kubernetes/pki/apiserver-etcd-client.crt --key /etc/kubernetes/pki/apiserver-etcd-client
.key --cacert /etc/kubernetes/pki/etcd/ca.crt get /registry/secrets/default/username
/registry/secrets/default/username
k8s


v1Secret�
�
usernamedefault"*$fafd61f3-49de-4821-8266-32d39391dcbd2�ݳ�a
kubectl-createUpdatev�ݳFieldsV1:-
+{"f:data":{".":{},"f:user":{}},"f:type":{}}B
useelrikoseOpaque"
```

`elrikose` is in the secret.

https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

You can now encrypt etcd at rest by using an `EncryptionConfiguration` resource and then setting `--encryption-provider-config` for the Kubernetes API server manifest to specify it.

Create a file on the controller node like `/etc/kubernetes/etcd/ec.yaml`

Add the config to the Kube API Server:

```yaml
  --encryption-provider-config=/etc/kubernetes/etcd/ec.yaml
```

You then have to volume mount the `/etc/kubernetes/etcd` folder in the API server

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
      - configmaps
    providers:
      - aescbc:
          keys:
            - name: key1
              # See the following text for more details about the secret value
              secret: <BASE 64 ENCODED SECRET>
      - identity: {} # this fallback allows reading unencrypted secrets;
                     # for example, during initial migration
```

Secrets and configmaps would be encrypted with `aescbc` and everything else would not. If identity would be listed first, nothing would be encrypted.

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
      - configmaps
    providers:
      - identity: {}
      - aescbc:
          keys:
            - name: key1
              # See the following text for more details about the secret value
              secret: <BASE 64 ENCODED SECRET>
```

NOTE: The password that you select here has to be one of 16, 24, or 32 characters long or you'll get an error.

If you want to replace all the secrets so they are encrypted or decrypted after you change the `--encryption-provider-config`, you would do this:

```sh
kubectl get secrets -A -ojson | kubectl replace -f -
```
