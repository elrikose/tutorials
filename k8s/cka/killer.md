# Killer.sh Simulator

Here are a couple of YouTube videos of people who took the [killer.sh](https://killer.sh) CKA simulator and recorded it:

- https://www.youtube.com/watch?v=uUUwvPUcTBg
- https://www.youtube.com/watch?v=EZ5mOR08QdQ

At 4 hours, the first video is very complete and proves that even a person who knows what they are doing can't complete the exam without knowing all of this like the back of their hand. The second video is only 2 hours and the user only successfully made it poorly through about 16 out of 25 questions.

The videos also show that the simulator UI is flakey, including:

- Multi-line cut and paste from the questions area to the Terminal.
- The notepad is often needed for an intermediate paste to keep line formatting working
- The notepad was irrecoverable at one point and required intervention from the proctor.
- Multi-terminal support is available, but very basic. I am still going to try to get better at using `tmux`.

# Notes

Below I have tried to craft the questions to be more useable for the 2 node cluster that I create locally. The cluster is created via Ubuntu `multipass` based scripts in my Github repository and should be rather portable:

https://github.com/emartin-hv/devops/tree/main/k8s

The scripts require at least 4 GB of RAM (2 GB per node) and a healthy bit of storage,

Almost every question is relevant to my cluster except the troubleshooting where you have to fix a __broken__ cluster. In the questions, I have also renamed K8s resources and abbreviated the text in the questions to simplify them for my needs. Next to each section header is the weight of the question on the test. Note two things:

- The higher point questions (8-10%) are toward the end of the exam
- You don't have to go in order, but must manually keep track of the answers

## Q1: Kube Contexts (1%)

>Your kubeconfig has multiple contexts. Dump a column of names of all of the contexts into `/exam/1/contexts`:

```sh
kubectl config get-contexts > /exam/1/contexts
# Clean up the context
```

>Write a shell script that will print the **current** context into `/exam/1/kubectl_default_context.sh`

```sh
kubectl config current-context > /exam/1/default_context.sh
```

>Now do the same thing without using `kubectl`

```sh
cat ~/.kube/config | grep -i "current-context" | awk '{print $2}'
```

## Q2: Pod Creation (3%)

>Create a pod with image `nginx:1.22.1` in namespace `q2` with a pod name of `nginx` and a container name of `nginx-container`. It must only be scheduled on the master node.

```sh
kubectl create ns q2
kubectl run nginx --image nginx:1.22.1 -n q2 --dry-run=client -o yaml > nginx-q2.yaml

# Edit nginx.yaml to change container name and set nodeName to control plane

kubectl apply -f nginx-q2.yaml
```

>Explain why Pods aren't scheduled on the control plane by default in `/exam/2/scheduler_reason`:

Master node is tainted

```
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
  - effect: NoSchedule
    key: node-role.kubernetes.io/control-plane
```

## Q3: Scale Pods (1%)

>With two pods running in a replica set on namespace `q3`, scale down from 2 to 1

```sh
# First create the deployment namespace and deployment
kubectl create ns q3
kubectl create deployment nginx -n q3 --image nginx --replicas=2 --dry-run=client -o yaml > nginx-q3.yaml
kubectl apply -f nginx-q3.yaml

<Wait for them both to be running>

# Scale it down
kubectl scale deployment nginx --replicas=1
```

>Now do the same for a running stateful set named `nginx-ss` in `q3`:

```sh
kubectl scale nginx-ss -n q3 --replicas=1
```

## Q4: Liveness and Readiness Probes

>Create a pod named `nginx-probes` with image `nginx:1.22.1` in namespace `q4`. It must contain a liveness probe (returns true) and a readiness probe which checks service URL `http://nginx-probes-service:80`.

```sh
kubectl create ns q4

kubectl run nginx-probes --image=nginx:1.22.1 -n q4--dry-run=client -o yaml > nginx-q4.yaml
```

Add the liveness and readiness probe section:

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx-probes
  name: nginx-probes
  namespace: q4
spec:
  containers:
  - image: nginx:1.22.1
    name: nginx-probes
    livenessProbe:
      exec:
        command:
        - "true"
    readinessProbe:
      exec:
        command:
        - wget
        - -T2
        - -O-
        - http://nginx-probes-service:80
      initialDelaySeconds: 5
      periodSeconds: 5
```

>Create another pod named `nginx-ready` with image `nginx:1.22.1` in namespace `q4` and label `app: probes`

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: nginx-ready
  name: nginx-ready
  namespace: q4
spec:
  containers:
  - image: nginx:1.22.1
    name: nginx-ready
```

>Create a service named `nginx-probes-service` that uses a selector of the label `app: probes`. Test to see if the readiness probe allows `nginx-probes` to be running.

```
kubectl expose pod nginx-ready -n q4 --port=80 --target-port=80 -n kube-system --dry-run=client -o yaml
```

And then edit the labels

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nginx-ready
  name: nginx-probes-service
  namespace: q4
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx-ready
```

## Q5: Sorting (1%)

>Write a script in `/exam/5/pods_by_date.sh` that lists all pods by creation date (`metadata.creationTimestamp`).

```sh
kubectl get pods -A --sort-by .metadata.creationTimestamp

cat << EOF > /exam/5/pods_by_date.sh
kubectl get pods -A --sort-by .metadata.creationTimestamp
EOF
chmod -x pods_by_date.sh
```

>Write a script in `/exam/5/pods_by_uid.sh` that lists all pods sorted by uid (`metadata.uid`).

```sh
kubectl get pods -A --sort-by .metadata.creationTimestamp

cat << EOF > /exam/5/pods_by_uid.sh
kubectl get pods -A --sort-by .metadata.creationTimestamp
EOF
chmod -x pods_by_uid.sh
```

## Q6: Persistent Volumes and Persistant Volume Claims (8%)

>Create a PV named `nginx-data-volume` with a capacity of `1Gi` and an access mode of `ReadWriteOnce`. The hostPath will be `/mnt/data` with no storage class.

https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
   name: nginx-data-volume
spec:
   capacity:
      storage: 1Gi
   accessModes:
      - ReadWriteOnce
   persistentVolumeReclaimPolicy: Retain
   hostPath:
      path: "/mnt/data" 
```

>Create a PVC named `nginx-data-pvc` in the namespace `q6` requesting `1Gi` with an access mode of ReadWriteOnce with no storage class.

https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolumeclaim


```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  creationTimestamp: null
  name: q6
spec: {}
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nginx-data-pvc
  namespace: q6
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

>Create a deployment named `nginx` with an image of `nginx:1.22.1` in namespace `q6` which mounts the PV as `/tmp/data`

https://kubernetes.io/docs/concepts/storage/persistent-volumes/#claims-as-volumes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: nginx
  name: nginx
  namespace: q6
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:1.22.1
        name: nginx
        resources: {}
        volumeMounts:
        - mountPath: "/tmp/data"
          name: nginx-data
      volumes:
      - name: nginx-data
        persistentVolumeClaim:
          claimName: nginx-data-pvc
status: {}
```

## Q7: Observability (1%)

>Install metrics-server

```sh
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Add the following `- --kubelet-insecure-tls` to the metrics-server arguments

```sh
kubectl apply -f components.yaml
```

Update the kube-api-server on the control node. Add the following to `/etc/kubernetes/manifests/kube-apiserver.yaml`

```yaml
    - --enable-aggregator-routing=true
```

>The metrics-server has been installed on the cluster. Show node resource usage via shell script `/exam/7/node_usage.sh`.

```sh
cat << EOF > /exam/7/node_usage.sh
kubectl top nodes
EOF
chmod +x /exam/7/node_usage.sh
```

>Show pod usage via shell script `/exam/7/pod_usage.sh`.

```sh
cat << EOF > /exam/7/pod_usage.sh
kubectl top pods
EOF
chmod +x /exam/7/pod_usage.sh
```

## Q8: Control Plane (2%)

>Login to the control plane node and report how the kubelet, scheduler, controller, etcd, are all started. Also find out the name of the DNS application on master node. Report in the file `/exam/8/report.txt`:

```
kubelet: [TYPE]
kube-apiserver: [TYPE]
kube-scheduler: [TYPE]
kube-controller-manager: [TYPE]
etcd: [TYPE]
dns: [TYPE] [NAME]
```

>Type would be one of `not-installed`, `process`, `static-pod`, `pod`

```
kubelet: process
kube-apiserver: static-pod
kube-scheduler: static-pod
kube-controller-manager: static-pod
etcd: static-pod
dns: pod coredns
```

## Q9: Manual Scheduling (5%)

>Temporarily stop the kube-scheduler so that it can be restarted.

```sh
mv /etc/kubernetes/kube-scheduler.yaml ~
```

>Create a single pod name `nginx-schedule` with an image of `nginx:1.22.1` and a namespace of `q9`. Confirm that it is not running/scheduled.

```sh
# First create the deployment namespace and deployment
kubectl create ns q9
kubectl run nginx-schedule -n q9 --image nginx:1.22.1  --dry-run=client -o yaml > nginx-q9.yaml
```

>Manually schedule the pod on `controlplane` node

Edit `nginx-q9.yaml` and add `nodeName:` to the yaml file:

```yaml
spec:
  nodeName: k8s
  containers:
  - image: nginx:1.22.1
```

And now apply it:

```sh
kubectl apply -f nginx-q9.yaml
```

>Restart the scheduler and create a new pod called `nginx-schedule2` in `q9` namespace to confirm that the scheduler is working

```sh
mv ~/kube-scheduler.yaml /etc/kubernetes

kubectl run nginx-schedule2 -n q9 --image nginx:1.22.1
```

## Q10: Service Accounts (6%)

>Create a ServiceAccount in namespace `q10` named `nginx-service-account`

https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/

```sh
kubectl create ns q10

kubectl create sa nginx-service-account -n q10 --dry-run=client -o yaml > nginx-service-account.yaml
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-service-account
  namespace: q10
```

>Create a Role and RoleBinding in namespace `q10` named `nginx-role` and `nginx-role-binding`. They should only be allowed to create Secrets and ConfigMaps in namespace `q10`

https://kubernetes.io/docs/reference/access-authn-authz/rbac/

```sh
kubectl create role nginx-role -n q10 --resources secrets,configmaps --verbs create --dry-run=client -o yaml > nginx-role.yaml
```

```yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: q10
  name: nginx-role
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["secrets", "configmaps"]
  verbs: ["create"]
```

And now the role binding

```
kubectl create rolebinding nginx-role-binding -n q10 --role nginx-role --serviceaccount q10:nginx-service-account --dry-run=client -o yaml > nginx-role-binding.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: nginx-role-binding
  namespace: q10
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: nginx-role
subjects:
- kind: ServiceAccount
  name: nginx-service-account
  namespace: q10
```

>Validate that the service account can create a secret or configmap, but not a pod:

```sh
$ kubectl auth can-i create secret -n q10 --as nginx-service-account
yes
$ kubectl auth can-i create configmaps -n q10 --as nginx-service-account
yes
$ kubectl auth can-i create pods -n q10 --as nginx-service-account
no
```

## Q11: DaemonSet with resource Limits (4%)

>Create a DaemonSet `nginx` in namespace `q11` with an image of `nginx:1.22.1` and labels `app:nginx-n11`. Pods should only require `10m` CPU and `10MiB` memory.

https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nginx
  namespace: q11
  labels:
    app: nginx-n11
spec:
  selector:
    matchLabels:
      app: nginx-n11
  template:
    metadata:
      namespace: n11
      labels:
        app: nginx-n11
    spec:
      tolerations:
      # these tolerations are to have the daemonset runnable on control plane nodes
      # remove them if your control plane nodes should not run pods
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      containers:
      - name: nginx
        image: nginx:1.22.1
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 10m
            memory: 10Mi
      terminationGracePeriodSeconds: 30
```

# Q12: Deployment simulating a DaemonSet

>Create a deployment named `nginx-deploy` with 2 replicas. The pods should have 2 containers `nginx:1.22.1` and `kubernetes/pause`, named `nginx` and `pause` respectively. It should be labeled with `app:nginx-important` Only one pod should run on each worker node, not control plane. So if there is only 1 worker node, the second pod should be unscheduled.

I had to look this one up because it is not clear:

https://stackoverflow.com/questions/58748447/simulating-daemonset-behaviour-with-kind-deployment

https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#types-of-inter-pod-affinity-and-anti-affinity

Create the deployment:

```sh
kubectl create ns q12
kubectl create deployment nginx-deploy --image nginx:1.22.1 --dry-run=client -o yaml > nginx-deploy-q12.yaml
```

And then add the labels, the second container, pod antiAffinity and topology keys

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: q12
  labels:
    app: nginx-important
  name: nginx-deploy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-important
  template:
    metadata:
      labels:
        app: nginx-important
    spec:
      containers:
      - image: nginx:1.22.1
        name: nginx
      - image: kubernetes/pause
        name: pause
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - nginx-important
            topologyKey: "kubernetes.io/hostname"
```

The pod should fail with the following error in `kubectl describe nginx-deploy-xxxx -n q12` pod:

>Warning  FailedScheduling  45s (x2 over 46s)  default-scheduler  0/2 nodes are available: 1 node(s) didn't match pod anti-affinity rules, 1 node(s) had untolerated taint {node-role.kubernetes.io/master: }. preemption: 0/2 nodes are available: 1 No preemption victims found for incoming pod, 1 Preemption is not helpful for scheduling.

# Q13: Multi-container Pod with Volumes (4%)

>Create a multi-container Pod in the namespace `q13` named `multi-container`. The containers should be named `nginx`, `busybox-writer`, and `busybox-reader` with images of `nginx:1.22.1`, `busybox:1.31.1`, and `busybox:1.31.1` respectively. The pod should have a volume that is not persisted or shared between pods. The `nginx` pod have an environment variable `POD_NODE_NAME` set to the nodename of the pod. The `busybox-writer` pod should output the date to a log file every second in a shared volume using `while true; do date >> /var/log/date.log; sleep 1; done`. The `busybox-reader` should just tail the `/var/log/date.log` file.

```sh
kubectl create ns q13
kubectl run -n q13 multi-container --image nginx:1.22.1 --dry-run=client -o yaml > multi-container-q13.yaml
```

This requires the use of an emptyDir volume: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-configuration-example

```yaml
spec:
  containers:
  - image: nginx
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 500Mi
```

And exposing pod info through environment: https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/

```yaml
        - name: MY_NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: multi-container
  name: multi-container
  namespace: q13
spec:
  containers:
  - image: nginx:1.22.1
    name: nginx
    env:
    - name: MY_NODE_NAME
      valueFrom:
        fieldRef:
            fieldPath: spec.nodeName
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  - image: busybox:1.31.1
    name: busybox-writer
    command: [ "sh", "-c" ]
    args: ["while true; do date >> /cache/date.log; sleep 1; done"]
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  - image: busybox:1.31.1
    name: busybox-reader
    command: [ "sh", "-c" ]
    args: ["tail -f /cache/date.log"]
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir:
      sizeLimit: 500Mi
```

Validation for environment variable:

```sh
$ k exec -n q13 multi-container -c nginx -it -- /bin/sh
# env | grep MY_NODE_NAME
MY_NODE_NAME=node-1
```

Validation for cache reader:

```yaml
$ kubectl logs -c busybox-reader multi-container -n q13 -f
Mon Dec 26 20:43:07 UTC 2022
Mon Dec 26 20:43:08 UTC 2022
Mon Dec 26 20:43:10 UTC 2022
Mon Dec 26 20:43:11 UTC 2022
...
```

# Q14: Cluster Info (2%)

>Retrieve the following information from the cluster
>- How many controller nodes?
>- How many worker nodes?
>- What is the Service CIDR range?
>- Which CNI plugin is configured and where is its config file
>- Which suffix will be added to static pods for `node-1`

Controller/Worker count:

```
kubectl get nodes
```

Service CIDR:
```sh
$ kubectl describe kube-api | grep ip-range
      --service-cluster-ip-range=10.96.0.0/12
```

Which CNI Plugin
```sh
kubectl get pods -n kube-system
kubectl describe pod <weave, flannel, etc>
```

Suffix: `-node-1`

## Q15: Event (3%)

>Write a command into `/exam/15/all_events.sh` that list all cluster events ordered by time.

```sh
echo "kubectl get events -A --sort-by .metadata.creationTimestamp" > /exam/15/all_events.sh
```

>Kill `kube-proxy` Pod and write the events to `/exam/15/proxy_pod_kill.log`

```sh
kubectl delete pod kube-proxy-xxxxx -n kube-system

/exam/15/all_events.sh > /exam/15/proxy_pod_kill.log
```

>Kill `kube-proxy` containerd container and write the events to `/exam/15/proxy_container_kill.log`

```sh
ssh node-1
sudo crictl rm -f 817cfee0a8ed5
exit

/exam/15/all_events.sh > /exam/15/proxy_container_kill.log
```

## Q16: Resources (2%)

>Write the names of all namespaced K8s resources (Pod, Secret) into `/exam/16/resources.txt`

```sh
kubectl api-resources --namespaced=true | awk '{ print $1 }' > /exam/16/resources.txt
```

>Find the namespace with the highest number of Roles and write the name and the number of roles to `/exam/16/roles.txt`

```
kubectl get role -A 
```

## Q17: Using crictl (3%)

>Launch a Pod named `nginx-containerd` in namespace `q17` with image `nginx:1.22.1` and with labels `pod=container` and `container=pod`. 

```sh
kubect create ns q17
kubectl run nginx-containerd --labels "pod=container,container=pod" -n q17 --image "nginx:1.22.1" --dry-run=client -o yaml > nginx-q17.yaml
kubectl apply -f nginx-q17.yaml
```

>Using `crictl` on the worker node, write the ID of the container and the `info.runtimeType` into `/exam/17/nginx-pod-container.txt`. Write the logs of the containter into `/exam/17/nginx-pod-container.log`.

```shell
# Log into worker
ssh node-1

# List logs
crictl ps 

# Dump logs in
crictl logs <container-id>

# Get Container runtimeType
$ sudo crictl inspect c096e5e6af726 | grep runtimeType
    "runtimeType": "io.containerd.runc.v2"
```

# Q18: Kubelet is Broken (%8)

>The kubelet on the worker node is not working. Fix and launch a pod to confirm it is working. Put the reason for the failure in `/exam/18/reason.txt`

Things to run on the worker node:

```sh
ssh node-1

sudo systemctl status kubelet
sudo systemctl start kubelet

sudo journalctl -u kubelet
```

"Current command vanished from the unit file" is the error in the kubelet status. Also missing `/usr/local/bin/kubelet`. Do a `which kubelet` since it is in the path. Change the `kubelet.service` file.

```sh
sudo systemctl daemon-reload
sudo systemctl start kubelet
```

# Q19: Secret (3%)

>Create a pod named `nginx-secret` in a new namespace `q19` with an image of `nginx:1.22.1`.
>Create a new secret called `nginx-secret` in namespace `q19` and mount it to `nginx-secret` pod in the same namespace.
>Create a new secret called `nginx-secret2` in namespace `q19` with `user=user1` and `pass=1234`. These secrets should be available in the environment as `APP_USER` and `APP_PASS`, respectively.


```sh
# Create the namespace
kubectl create ns q19

# Secret number 1 - mounted
kubectl create secret generic nginx-secret -n q19 --from-literal halt=1234 --dry-run=client -o yaml > nginx-secret-q19.yaml

# Secret number 1 - env
kubectl create secret generic nginx-secret2 -n q19 --from-literal "user=user1" --from-literal "pass=1234" --dry-run=client -o yaml >> nginx-secret-q19.yaml

# Pod
kubectl run nginx-secret -n q19 --image nginx:1.22.1 --dry-run=client -o yaml >> nginx-secret-q19.yaml
```

Don't forget to add `---` separator lines in the yaml

```sh
kubectl apply -f nginx-secret-q19.yaml
```

Here is the manifest:

```yaml
---
apiVersion: v1
data:
  halt: MTIzNA==
kind: Secret
metadata:
  creationTimestamp: null
  name: nginx-secret
  namespace: q19
---
apiVersion: v1
data:
  pass: MTIzNA==
  user: dXNlcjE=
kind: Secret
metadata:
  creationTimestamp: null
  name: nginx-secret2
  namespace: q19
---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx-secret
  name: nginx-secret
  namespace: q19
spec:
  containers:
  - image: nginx:1.22.1
    name: nginx
    env:
    - name: APP_USER
      valueFrom:
        secretKeyRef:
          name: nginx-secret2
          key: user
    - name: APP_PASS
      valueFrom:
        secretKeyRef:
          name: nginx-secret2
          key: pass
    volumeMounts:
    - name: secret
      mountPath: "/tmp/secret1"
      readOnly: true
  volumes:
  - name: secret
    secret:
      secretName: nginx-secret
```

# Q20: Upgrade Worker Node (10%)

>A worker node is running an older version of Kubernetes and is not part of the cluster. Upgrade it to the same version and add it to the cluster

The kubelet on the worker node was v1.23.1 and the master and other worker node was 1.24.1. `kubeadm` was already at `1.24.1`, but the kubelet was at `1.23.1`.

```sh
ssh node-1

sudo apt update -y
sudo apt install kubeadm=1.24.1-00 # Not needed, but in case

sudo kubeadm upgrade plan
sudo kubeadm upgrade node v1.24.1

sudo apt install kubelet=1.24.1-00

sudo systemctl daemon-reload
sudo systemctl restart kubelet

# Login to master and get join command
ssh master 
kubeadm token create --print-join-command

# On worker run join command and uncordon
kubeadm join ...
kubectl uncordon node-1


```

# Q21: NodePort Service (2%)

>Create a static pod named `nginx-static` in namespace `q21` on the controller node. The image should be `nginx:1.22.1` and have resource requests of `10m` CPU and `20Mi` of memory.

```sh
# Create the namespace
kubectl create ns q21

# Login to the master node
ssh node-1

kubectl run nginx-static -n q21 --image nginx:1.22.1 --dry-run=client -o yaml > nginx-static.yaml
```

Add `namespace:` and `resources:` requests:

https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#example-1

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  namespace: q21
  labels:
    run: nginx-static
  name: nginx-static
spec:
  containers:
  - image: nginx:1.22.1
    name: nginx-static
    resources:
      requests:
        cpu: 10m
        memory: 20Mi
```

>Expose a NodePort called `nginx-service` which exposes port 80. Make sure the endpoints are accessible on the master IP.

https://kubernetes.io/docs/concepts/services-networking/service/#nodeport-custom-port

```sh
kubectl expose pod nginx-service --type=NodePort --target-port=80 --port=80 -n q21 --dry-run=client -o yaml > nginx-static-q21.yaml
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: q21
spec:
  type: NodePort
  selector:
    run: nginx-static
  ports:
      # By default and for convenience, the `targetPort` is set to the same value as the `port` field.
    - port: 80
      targetPort: 80
      nodePort: 30007
```

# Q22: Certificates with kubeadm (2%)

>Check the certificates on the `kube-apiserver` using `openssl` and when they will expire. Write the expiration date into `/exam/q22/expiration`.

```sh
ubuntu@k8s:~$ cat /etc/kubernetes/pki/apiserver.crt | openssl x509 -noout -dates
notBefore=Dec 24 17:58:20 2022 GMT
notAfter=Dec 24 17:58:20 2023 GMT
```

>Confirm with what `kubeadm` shows

```sh
$ sudo kubeadm certs check-expiration
[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'

CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Dec 24, 2023 17:58 UTC   362d            ca                      no      
apiserver                  Dec 24, 2023 17:58 UTC   362d            ca                      no      
apiserver-etcd-client      Dec 24, 2023 17:58 UTC   362d            etcd-ca                 no      
apiserver-kubelet-client   Dec 24, 2023 17:58 UTC   362d            ca                      no      
controller-manager.conf    Dec 24, 2023 17:58 UTC   362d            ca                      no      
etcd-healthcheck-client    Dec 24, 2023 17:58 UTC   362d            etcd-ca                 no      
etcd-peer                  Dec 24, 2023 17:58 UTC   362d            etcd-ca                 no      
etcd-server                Dec 24, 2023 17:58 UTC   362d            etcd-ca                 no      
front-proxy-client         Dec 24, 2023 17:58 UTC   362d            front-proxy-ca          no      
scheduler.conf             Dec 24, 2023 17:58 UTC   362d            ca                      no      

CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
ca                      Dec 21, 2032 17:58 UTC   9y              no      
etcd-ca                 Dec 21, 2032 17:58 UTC   9y              no      
front-proxy-ca          Dec 21, 2032 17:58 UTC   9y              no
```

>Write the `kubeadm` renewal command of the cert into `/exam/22/renewcerts.sh`

```sh
echo "kubectl certs renew apiserver" > /exam/22/renewcerts.sh
chmod +x /exam/22/renewcerts.sh
```

# Q23: Certificates (2%)

>Node `node-1` has been added with `kubeadm` and TLS. Find the "Issuer" and "Extended Key Usage" values for:
> - kubelet client certificate - outgoing to api server
> - kubelet server certificate - incoming from api server
> Write the information to `/exam/23/cert-info.txt`

Client found in `/etc/kubernetes/kubelet.conf`:

```sh
$ cat /var/lib/kubelet/pki/kubelet-client-current.pem | openssl x509 -text -noout
...
        Issuer: CN = kubernetes
...
            X509v3 Extended Key Usage: 
                TLS Web Client Authentication
```

Server found in `/etc/kubernetes/kubelet.conf`:

```sh
$ cat /var/lib/kubelet/pki/kubelet-client-current.pem | openssl x509 -text -noout
...
        Issuer: CN = kubernetes
...
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment, Certificate Sign
```

# Q24: Network Policy (9%)

>Create a network policy `backend-policy` in namespace `q24` that only allows the backend to
> - Connect to `db1-*` pods on port 1111
> - Connect to `db1-*` pods on port 2222
> Use the `app` label in your policy


# Q25: ETCD Backup (8%)

>Make a backup of etcd running on the `k8s` master and save it to `/tmp/etcd-backup.db`.

```sh
# SSH into master
ssh k8s

ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/server.crt \
     --key=/etc/kubernetes/pki/etcd/server.key \
     snapshot save /tmp/etcd-backup.db


```


>Create a pod and then restore the database to see it disappear

Create pod:

```sh
kubectl create ns q25
kubectl run nginx --image=nginx --label app=nginx -n q25 --dry-run=client -o yaml > nginx-etcd-q25.yaml
kubectl apply -f nginx-etcd-q25.yaml
```

Now restore. Find the restore path in the etcd manifest

```
ETCDCTL_API=3 etcdctl \
     snapshot restore /tmp/etcd-backup.db --data-dir /var/lib/etcdrestored
```

Change the etcd hostPath to `/var/lib/etcdrestored` in the static manifest file

# Extra Question 1

>Check all pods in a namespace `q13` and find the names that would probably be terminated first if the Node ran out of resources (CPU or memory). Write the pods in `/exam/extra/1/unstable-pods.txt`.