# CKA Mock Exam 2

1. Take a backup of the etcd cluster and save it to `/opt/etcd-backup.db`.

```sh
ETCDCTL_API=3 etcdctl snapshot save /opt/etcd-backup.db --endpoints https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

2. Create a Pod called redis-storage with image: `redis:alpine` with a Volume of type emptyDir that lasts for the life of the Pod. Specs below.
- Pod named `redis-storage` created
- Pod `redis-storage` uses Volume type of emptyDir
- Pod `redis-storage` uses volumeMount with mountPath = `/data/redis`

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: redis-storage
  name: redis-storage
spec:
  containers:
  - image: redis:alpine
    name: redis-storage
    resources: {}
    volumeMounts:
    - mountPath: /data/redis
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 10Mi
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

3. Create a new pod called `super-user-pod` with image `busybox:1.28`. Allow the pod to be able to set system_time. The container should `sleep` for `4800` seconds.
- Pod: `super-user-pod`
- Container Image: `busybox:1.28`
- `SYS_TIME` capabilities for the conatiner?

```sh
k run super-user-pod --image busybox:1.28 $DO -- sleep 4800 > super-user-pod.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: super-user-pod
  name: super-user-pod
spec:
  containers:
  - args:
    - sleep
    - "4800"
    image: busybox:1.28
    name: super-user-pod
    securityContext:
      capabilities:
        add: ["SYS_TIME"]
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

4. A pod definition file is created at `/root/CKA/use-pv.yaml`. Make use of this manifest file and mount the persistent volume called pv-1. Ensure the pod is running and the PV is bound.
- mountPath: `/data` 
- persistentVolumeClaim Name: `my-pvc` 
- persistentVolume Claim configured correctly
- pod using the correct mountPath
- pod using the persistent volume claim?

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 10Mi
  storageClassName: ""
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: use-pv
  name: use-pv
spec:
  containers:
  - image: nginx
    name: use-pv
    resources: {}
    volumeMounts:
      - mountPath: "/data"
        name: my-pvc
  volumes:
    - name: my-pvc
      persistentVolumeClaim:
        claimName: my-pvc
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

5. Create a new deployment called nginx-deploy, with image nginx:1.16 and 1 replica. Next upgrade the deployment to version 1.17 using rolling update.
- Deployment : nginx-deploy. Image: nginx:1.16
Image: nginx:1.16
Task: Upgrade the version of the deployment to 1:17
Task: Record the changes for the image upgrade

```sh
k create deployment nginx-deploy --image nginx:1.16 --replicas 1 $DO > nginx-deploy.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nginx-deploy
  name: nginx-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-deploy
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx-deploy
    spec:
      containers:
      - image: nginx:1.16
        name: nginx
        resources: {}
status: {}
```

```sh
k edit -f nginx-deploy.yaml 
k rollout status deploy nginx-deploy
```

6. Create a new user called `john`. Grant him access to the cluster. John should have permission to `create`, `list`, `get`, `update` and `delete` pods in the `development` namespace . The private key exists in the location: `/root/CKA/john.key` and csr at `/root/CKA/john.csr`. 
Important Note: As of kubernetes 1.19, the CertificateSigningRequest object expects a signerName.

Please refer the documentation to see an example. The documentation tab is available at the top right of terminal.
- CSR: `john-developer` Status:Approved
- Role Name: developer, namespace: development, Resource: Pods
- Access: User `john` has appropriate permissions

```sh
cat CKA/john.csr | base64 | tr -d '\n'
```

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  request: LS0t...
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - client auth
```

```sh
k create role --verb=create,list,get,update,delete --resource=pods -n development developer $DO > developer-role.yaml
k create rolebinding developer-rb  --role developer --user john -n development $DO > developer-rb.yaml
k apply -f developer-role.yaml 
k apply -f developer-rb.yaml 
```

Test:

```sh
k auth can-i create pods --as john -n development
k auth can-i delete pods --as john -n development
k auth can-i create deploy --as john -n development
k auth can-i create deploy --as john -n default
k auth can-i create deploy --as john -n kube-system
k auth can-i create deploy --as john -n default
```

7. Create a nginx pod called `nginx-resolver` using image `nginx`, expose it internally with a service called `nginx-resolver-service`. Test that you are able to look up the service and pod names from within the cluster. Use the image: `busybox:1.28` for dns lookup. Record results in `/root/CKA/nginx.svc` and `/root/CKA/nginx.pod`
- Pod: nginx-resolver created
- Service DNS Resolution recorded correctly
- Pod DNS resolution recorded correctly

```sh
k run nginx-critical --image nginx $DO
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx-critical
  name: nginx-critical
spec:
  containers:
  - image: nginx
    name: nginx-critical
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

```sh
k run -it busybox --image=busybox:1.28 --restart=Never --rm -- nslookup nginx-resolver-service.default.svc
k run -it busybox --image=busybox:1.28 --restart=Never --rm -- nslookup 10-244-192-5.default.pod
```