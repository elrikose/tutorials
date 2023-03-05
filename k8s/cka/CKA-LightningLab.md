
# Cluster Upgrade to 1.26.0

Upgrade the current version of kubernetes from `1.25.0` to `1.26.0` exactly using the `kubeadm` utility. Make sure that the upgrade is carried out one node at a time starting with the controlplane node. To minimize downtime, the deployment `gold-nginx` should be rescheduled on an alternate node before upgrading each node.
Upgrade controlplane node first and drain node node01 before upgrading it. Pods for `gold-nginx` should run on the controlplane node subsequently.

```sh
kubectl cordon controlplane
sudo apt update -y
sudo apt install kubeadm=1.26.0-00
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.26.0
...
sudo apt install kubelet=1.26.0-00 kubectl=1.26.0-00

sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

Now upgrade the node:

```sh
ssh node01

sudo apt update -y
sudo apt install kubeadm=1.26.0-00
sudo kubeadm upgrade node
sudo apt install kubelet=1.26.0-00

...

sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

# Custom Columns

Print the names of all deployments in the admin2406 namespace in the following format:

DEPLOYMENT CONTAINER_IMAGE READY_REPLICAS NAMESPACE

<deployment name> <container image used> <ready replica count> <Namespace>
. The data should be sorted by the increasing order of the deployment name.
Example: 

DEPLOYMENT CONTAINER_IMAGE READY_REPLICAS NAMESPACE
deploy0 nginx:alpine 1 admin2406
Write the result to the file /opt/admin2406_data.


```sh
k get deploy -n admin2406 -o=custom-columns='DEPLOYMENT:.metadata.name,CONTAINER_IMAGE:.spec.template.spec.containers[0].image,READY_REPLICAS:.status.availableReplicas,NAMESPACE:.metadata.namespace' > /opt/admin2406_data
```

# Kubeconfig issue

A kubeconfig file called admin.kubeconfig has been created in /root/CKA. There is something wrong with the configuration. Troubleshoot and fix it.
Fix /root/CKA/admin.kubeconfig

Change port number to 6443

# Update the deployment image

Create a new deployment called `nginx-deploy`, with image `nginx:1.16` and `1` replica. Next upgrade the deployment to version `1.17` using rolling update.

```sh
kdo create deploy nginx-deploy --image nginx:1.16 --replicas 1 -n default > nginx-deploy.yaml
```

Then `kubectl edit` the deployment and change the image to nginx:1.17

# Deployment with PVC problems

A new deployment called `alpha-mysql` has been deployed in the `alpha` namespace. However, the pods are not running. Troubleshoot and fix the issue. The deployment should make use of the persistent volume `alpha-pv` to be mounted at `/var/lib/mysql` and should use the environment variable `MYSQL_ALLOW_EMPTY_PASSWORD=1` to make use of an empty root password.
Important: Do not alter the persistent volume.

```sh
k get pvc -n alpha alpha-claim -o yaml > mysql-alpha-pvc.yaml

Change PVC Name
Change ReadWriteMany -> ReadWrite Once
Change Storage Class Name
```

# ETCD Backup

Take the backup of ETCD at the location `/opt/etcd-backup.db` on the controlplane node.

```sh
ETCDCTL_API=3 etcdctl snapshot save /opt/etcd-backup.db --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt  --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key
```

# Secret Volume

Create a pod called `secret-1401` in the `admin1401` namespace using the busybox image. The container within the pod should be called `secret-admin` and should `sleep` for `4800` seconds. 
The container should mount a read-only secret volume called `secret-volume` at the path `/etc/secret-volume`. The secret being mounted has already been created for you and is called `dotfile-secret`.

```sh
kubectl config set-context --current --namespace admin1401
kdo run secret-1401 --image busybox -- sh -c "sleep 4800" > secret-1401.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-1401
  name: secret-1401
spec:
  containers:
  - args:
    - sh
    - -c
    - sleep 4800
    image: busybox
    name: secret-admin
    resources: {}
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secret-volume"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
      optional: true
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Now test it by logging into the pod and checking the volume:

```sh
k exec secret-1401 -it -- /bin/sh
ls -l /etc/secret-volume
```
