# CKA Questions

This page has a list of random questions that I have found online and have tried to solve.

https://k21academy.com/docker-kubernetes/cka-ckad-exam-questions-answers/

Create a new service account with the name pvviewer. Grant this Service account access to list all PersistentVolumes in the cluster by creating an appropriate cluster role called pvviewer-role and ClusterRoleBinding called pvviewer-role-binding. Next, create a pod called pvviewer with the image: redis and serviceaccount: pvviewer in the default namespace.

```sh
# Create service account
$ kubectl create serviceaccount pvviewer

# Create cluster role
$ kubectl create clusterrole pvviewer-role --verb=list --resource=PersistentVolumes


# Create cluster role binding
$ kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer


# Verify
$ kubectl auth can-i list PersistentVolumes –as system:serviceaccount:default:pvviewer
```

- Create a new deployment called `nginx-deploy`, with image `nginx:1.16` and 1 replica. Record the version. Next upgrade the deployment to version 1.17 using rolling update. Make sure that the version upgrade is recorded in the resource annotation.

```sh
kubectl create deploy nginx-deploy --image=nginx:1.16 --replicas=1 $DO
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
      labels:
        app: nginx-deploy
    spec:
      containers:
      - image: nginx:1.16
        name: nginx
```

Now do the rolling update:

```sh
kubectl set image deployment nginx-deploy nginx=nginx:1.16 --record
```

- Create snapshot of the etcd running at https://127.0.0.1:2379. Save snapshot into `/opt/etcd-snapshot.db`.

- Create a Persistent Volume with the given specification. Volume Name: `pv-analytics`, Storage: `100Mi`, Access modes: `ReadWriteMany`, Host Path: `/pv/data-analytics`

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-analytics
spec:
  capacity:
    storage: 100Mi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: manual
  hostPath:
    path: /pv/data-analytics
```

- Taint the worker node to be `Unschedulable`. Once done, create a pod called `dev-redis`, image `redis:alpine` to ensure workloads are not scheduled to this worker node. Finally, create a new pod called `prod-redis` and image `redis:alpine` with toleration to be scheduled on `node01`.

`key: env_type`, `value: production`, `operator: Equal`, and `effect: NoSchedule`

```sh
kubectl get nodes
kubectl taint node node01 env_type=production:NoSchedule
kubectl describe nodes node01 | grep -i taint
kubectl run dev-redis --image=redis:alpine --dyn-run=client -o yaml > pod-redis.yaml
```

```yaml
apiVersion: v1 
kind: Pod 
metadata:
  name: prod-redis 
spec:
  containers:
  - name:  prod-redis 
    image:  redis:alpine
  tolerations:
  - effect: NoSchedule 
    key: env_type 
    operator: Equal 
    value: production
```

- Set the node named worker node as unavailable and reschedule all the pods running on it. (Drain node)

```sh
$ kubectl drain worker node --ignore-daemonsets
```

- Create a Pod called `non-root-pod`, `image: redis:alpine`, `runAsUser: 1000`, `fsGroup: 2000`

- Create a NetworkPolicy which denies all ingress traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

1. Create a namespace called `development` and a pod with image `nginx` called nginx.

```sh
kubectl create namespace development
kubectl run nginx --image=nginx --restart=Never -n development
```

2. Create a `nginx` pod with label `env=test` in `engineering` namespace.

```sh
kubectl run nginx --image=nginx --restart=Never --labels=env=test --namespace=engineering --dry-run -o yaml > nginx-pod.yaml
kubectl create -f nginx-pod.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: engineering
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  restartPolicy: Never
```

3. Get list of all pods in all namespaces and write it to file `/opt/pods-list.yaml`

```sh
# Basic
$ kubectl get pod -A > /opt/pods-list.yaml

# Just the pod names
$ k get pod -A --no-headers | awk '{ print $2 }' > 
kube-flannel-ds-26tgh
kube-flannel-ds-cp276
coredns-57575c5f89-bq969
coredns-57575c5f89-pl2dp
etcd-k8s
kube-apiserver-k8s
kube-controller-manager-k8s
kube-proxy-fx82t
kube-proxy-kbxk7
kube-scheduler-k8s
metrics-server-5ccdd99954-skfqj
nginx
nginx-deploy-7cf5f89ccb-9nvrt
nginx-deploy-7cf5f89ccb-whr9z
```

4. Create a pod with image nginx called nginx and allow traffic on port 80

```sh
kubectl run nginx --image=nginx --restart=Never --port=80
kubectl expose pod nginx -n nginx-test --type=NodePort --port=80 --target-port=80
```

5. Create a busybox pod that runs the command `env` and save the output to `envpod` file

```sh
kubectl run busybox --image=busybox --restart=Never --rm -it -- env > envpod
```

`--restart=Never` is required or the pod will just restart

6. List pod logs named `frontend` and search for the pattern `started` and write it to a file `/opt/error-logs`

```sh
kubectl logs frontend | grep -i "started" > /opt/error-logs
```

7. Create a pod that echo `hello world` and then exits. Have the pod deleted automatically when it's completed

```sh
kubectl run busybox --image=busybox -it --rm --restart=Never -- /bin/sh -c 'echo hello world'
kubectl get po # You shouldn't see pod with the name "busybox"
```

8. Create a pod with environment variables as var1=value1. Check the environment variable in pod

```sh
kubectl run nginx --image=nginx --restart=Never --env=var1=value1

# Validate with any of these
kubectl exec -it nginx -- env 
kubectl exec -it nginx -- sh -c 'echo $var1'
kubectl describe po nginx | grep value1
```

9. Get list of all the pods showing name and namespace with a jsonpath expression.

```sh
kubectl get pods -o=jsonpath="{.items[*]['metadata.name' , 'metadata.namespace']}"
```

10. Check the image version in pod without the describe command

```sh
kubectl get po nginx -o jsonpath='{.spec.containers[].image}{""}'
```

11. List the nginx pod with custom columns POD_NAME and POD_STATUS

```sh
kubectl get po -o=custom-columns="POD_NAME:.metadata.name, POD_STATUS:.status.containerStatuses[].state"
```

12. List all the pods sorted by name

```sh
kubectl get pods --sort-by=.metadata.name
```

13. Create a pod that having 3 containers in it? (Multi-Container) `image=nginx`, `image=redis`, `image=consul` name nginx container as `nginx-container` Name redis container as `redis-container` Name consul container as `consul-container` Create a pod manifest file for a container and append container section for rest of the images 

```sh
kubectl run multi-container --generator=run-pod/v1 --image=nginx -- dry-run -o yaml > multi-container.yaml 
```

Edit multi-container.yaml 

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multi-container
    name: multi-container
spec:
  containers:
   - image: nginx
     name: nginx-container
   - image: redis
     name: redis-container
   - image: consul
     name: consul-container
  restartPolicy: Always
```
14. Create 2 nginx image pods in which one of them is labelled with `env=prod` and another one labelled with `env=dev` and verify the same.

```sh
kubectl run --image=nginx labels=env=prod nginx-prod --dry-run -o yaml > nginx-prod.yaml
```

Now, edit nginx-prod.yaml file and remove entries like "creationTimestamp: null" "dnsPolicy: ClusterFirst"
 
 ```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    env: prod
  name: nginx-prod
spec:
 containers:
  - image: nginx
    name: nginx-prod
    restartPolicy: Always
```

Generate nginx-dev:

```sh
kubectl run --image=nginx labels=env=dev nginx-dev --dry-run -o yaml > nginx-dev.yaml
```

Now, edit nginx-dev.yaml file and remove entries like "creationTimestamp: null" "dnsPolicy: ClusterFirst"
 
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    env: prod
  name: nginx-dev
spec:
 containers:
  - image: nginx
    name: nginx-dev
    restartPolicy: Always
```

    
Verify:

```sh
kubectl get po -l env=prod
kubectl get po -l env=dev
```

15. Get IP address of the pod - `nginx-dev`

```sh
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"t"}{.status.podIP}{""}{end}'
```

16. Print pod name and start time to `/opt/pod-status`

```sh
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"t"}{.status.podIP}{""}{end}'
```

17. Check the Image version of `nginx-dev` pod using jsonpath

```sh
kubectl get po nginx-dev -o jsonpath='{.spec.containers[].image}{""}'
```

18. Create a `busybox` pod and add `sleep 3600` command

```sh
kubectl run busybox --image=busybox --restart=Never -- /bin/sh -c "sleep 3600"
```

19. Create an nginx pod and list the pod with different levels of verbosity

```sh 
# create a pod 
kubectl run nginx --image=nginx --restart=Never --port=80

# List the pod with different verbosity 
kubectl get pod nginx --v=7
kubectl get pod nginx --v=8
kubectl get pod nginx --v=9
```

20. List the nginx pod with custom columns POD_NAME and POD_STATUS

```sh
kubectl get pod -o=custom-columns="POD_NAME:.metadata.name, POD_STATUS:.status.containerStatuses[].state"
```

21. List all the pods sorted by name

```sh
kubectl get pods --sort-by=.metadata.name
```

22. List all the pods sorted by created timestamp

```sh
kubectl get pods--sort-by=.metadata.creationTimestamp
```

23. List all the pods showing name and namespace with a json path expression
```sh
kubectl get pods -o=jsonpath="{.items[*]['metadata.name', 'metadata.namespace']}"
```

24. List `nginx-dev` and `nginx-prod` pod and delete those pods

```sh
kubectl get pods -o wide
kubectl delete po "nginx-dev"
kubectl delete po "nginx-prod"
```

25. Delete the pod without any delay (force delete)

```sh
kubectl delete po "POD-NAME" --grace-period=0 -force
```

26. Create a `redis` pod and expose it on port `6379`
```sh
kubectl run redis --image=redis --restart=Never --port=6379

kubectl expose pod redis --port=30000 --targetPort=6379
```

27. Create the `nginx` pod with version `1.17.4` and expose it on port 80

```sh
kubectl run nginx --image=nginx:1.17.4 --restart=Never -- port=80
```

28. Change the Image version to 1.15-alpine for the pod you just created and verify the image version is updated.

```sh
kubectl set image pod/nginx nginx=nginx:1.15-alpine
kubectl describe po nginx

# another way it will open vi editor and change the version 
kubectl edit po nginx
kubectl describe po nginx
```

29. Change the Image version back to 1.17.1 for the pod you just updated and observe the changes
```sh
kubectl set image pod/nginx nginx=nginx:1.17.1
kubectl describe po nginx
kubectl get po nginx -w # watch it
```

30. Create a redis pod, and have it use a non-persistent storage During exam, you will have access to kubernetes.io site, Refer : https://kubernetes.io/docs/tasks/configure-pod-container/configurevolume-storage/

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: redis
spec:
  containers:
  - name: redis
    image: redis
    volumeMounts:
    - name: redis-storage
      mountPath: /data/redis
    ports:
    - containerPort: 6379
  volumes:
  - name: redis-storage
    emptyDir: {}
```

31. Create a Pod with three busy box containers with commands "ls; sleep 3600;", "echo Hello World; sleep 3600;" and "echo this is the third container; sleep 3600" respectively and check the status

```sh
# first create single container pod with dry run flag 
kubectl run busybox --image=busybox --restart=Always --dry-run=client -o yaml -- bin/sh -c "sleep 3600; ls" > multi-container.yaml
```

Edit the pod to following yaml and create it

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: busybox
  name: busybox
spec:
  containers:
  - args:
    - bin/sh
    - -c
    - ls; sleep 3600
    image: busybox
    name: busybox-container-1
  - args:
     - bin/sh
     - -c
     - echo Hello world; sleep 3600
    image: busybox
    name: busybox-container-2
  - args:
    - bin/sh
    - -c
    - echo this is third container; sleep 3600
    image: busybox
    name: busybox-container-3
  restartPolicy: Always
```

32. Check logs of each container that "busyboxpod-{1,2,3}"

```sh
kubectl logs busybox -c busybox-container-1
kubectl logs busybox -c busybox-container-2
kubectl logs busybox -c busybox-container-3
```

33. Create a Pod with main container `busybox` and which executes this `while true; do echo "Hi I am from Main container'` >> /var/log/index.html; sleep 5; done" and with sidecar container with nginx image which exposes on port 80. Use emptyDir Volume and mount this volume on path /var/log for busybox and on path /usr/share/nginx/html for nginx container. Verify both containers are running.

```sh 
# create an initial yaml file with this
kubectl run multi-cont-pod --image=busbox --restart=Never -- dry-run -o yaml > multi-container.yaml

# edit the yml as below and create it
kubectl create -f multi-container.yaml

vim multi-container.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: multi-cont-pod
  name: multi-cont-pod
spec:
  volumes:
  - name: var-logs
    emptyDir: {}
  containers:
  - image: busybox
    command: ["/bin/sh"]
    args: ["-c", "while true; do echo 'Hi I am from Main container' >> /var/log/index.html; sleep 5;done"]
    name: main-container
    volumeMounts:
    - name: var-logs
      mountPath: /var/log
  - image: nginx
    name: sidecar-container
    ports:
    - containerPort: 80
    volumeMounts:
    - name: var-logs
      mountPath: /usr/share/nginx/html
  restartPolicy: Never
```

Create Pod  with `kubectl apply -f`
