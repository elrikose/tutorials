# Killer Coda Simulator and Scenarios

The [Killer Coda](https://killercoda.com/killer-shell-cka) CKA simulator has scenarios to help with testing the CKA.

# API Server Crash

Use the following debug if the K8s API Server or other components have crashed. Often when the API server has crashed you have to drop back out to the container runtime.

```sh
# This should fail if api server is down
kubectl -n kube-system get pod 

# This should show restarts or give a clue of what has failed
watch crictl ps -a
```

To find the problem check the pod logs on the file system. If you are fast enough get the container id from `crictl` and get the logs:

```sh
crictl ps -a
crictl logs 77e85d0408c32
```

The api server will fail on the following, but If the controller manager or etcd is down, you will get a CrashLoopBackOff:

```sh
$ k get pod -A 
NAMESPACE     NAME                                       READY   STATUS             RESTARTS        AGE
...
kube-system   kube-controller-manager-controlplane       0/1     CrashLoopBackOff   4 (35s ago)     2m4s
```

If the `--etcd-servers` is incorrect in the static manifest you will get something like this:

```
W0122 02:01:49.601695       1 logging.go:59] [core] [Channel #3 SubChannel #6] grpc: addrConn.createTransport failed to connect to {
  "Addr": "this-is-very-wrong",
  "ServerName": "this-is-very-wrong",
  "Attributes": null,
  "BalancerAttributes": null,
  "Type": 0,
  "Metadata": null
}. Err: connection error: desc = "transport: Error while dialing dial tcp: address this-is-very-wrong: missing port in address"
```

If the `yaml` is all busted it will look like this in `/var/log/syslog` when you search for apiserver:

```log
Jan 22 02:14:10 controlplane kubelet[24118]: E0122 02:14:10.672832   24118 file.go:187] "Could not process manifest file" err="/etc/kubernetes/manifests/kube-apiserver.yaml: couldn't parse as pod(yaml: line 2: mapping values are not allowed in this context), please check config file" path="/etc/kubernetes/manifests/kube-apiserver.yaml"
```

# Config Maps

- Create a ConfigMap named `trauerweide` with content tree=trauerweide
- Create the ConfigMap stored in existing file `/root/cm.yaml`

```sh
kdo create cm trauerweide --from-literal tree=trauerweide > tree.yaml
kaf /root/cm.yaml
```

```sh
kdo create cm trauerweide --from-literal tree=trauerweide > tree.yaml
kaf tree.yaml
configmap/trauerweide created
```

Make the pod via a `kubectl run`:

```sh
kdo run pod1 --image nginx:alpine > pod1.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod1
  name: pod1
spec:
  containers:
  - image: nginx:alpine
    name: pod1
    resources: {}
    env:
    - name: TREE1
      valueFrom:
        configMapKeyRef:
          name: trauerweide           # The ConfigMap this value comes from.
          key: tree
    volumeMounts:
    - name: birke
      mountPath: "/etc/birke"
  volumes:
  - name: birke
    configMap:
      name: birke
```

Now validate the `pod1` has the environment and the files in place:

```sh
$ k exec pod1 -it -- /bin/sh
# env | grep TR
TREE1=trauerweide
# ls -l /etc/birke
total 0
lrwxrwxrwx    1 root     root            17 Jan 29 01:45 department -> ..data/department
lrwxrwxrwx    1 root     root            12 Jan 29 01:45 level -> ..data/level
lrwxrwxrwx    1 root     root            11 Jan 29 01:45 tree -> ..data/tree
```

# Ingress Create

There are two existing Deployments in Namespace `world` which should be made accessible via an Ingress.

First: create ClusterIP Services for both Deployments for port 80 . The Services should have the same name as the Deployments.

```sh
k expose deployment asia --port 80
k expose deployment europe --port 80
```

Create a new Ingress resource called world for domain name `world.universe.mine`. The domain points to the K8s Node IP via `/etc/hosts` .The Ingress resource should have two routes pointing to the existing Services:

http://world.universe.mine:30080/europe/

and

http://world.universe.mine:30080/asia/

Don't forget the IngressClass name. That is what points the ingress to the right controller running in the cluster. In this example `ingressClassName: nginx` should be used since it is the only one found.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: world
  namespace: world
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: "world.universe.mine"
    http:
      paths:
      - path: /europe
        pathType: Prefix
        backend:
          service:
            name: europe
            port:
              number: 80
      - path: /asia
        pathType: Prefix
        backend:
          service:
            name: asia
            port:
              number: 80
```



# ServiceAccount / Role / RoleBindings

There are existing Namespaces `ns1` and `ns2`. Create ServiceAccount `pipeline` in both Namespaces.
These SAs should be allowed to `view` almost everything the cluster using the default ClusterRole `view` for this.
These SAs should be allowed to `create` and `delete` Deployments in their Namespace.
Verify everything using kubectl auth can-i .

First create the service accounts:

```sh
k create sa pipeline -n ns1 $DO > pipeline-ns1.yaml
k create sa pipeline -n ns2 $DO > pipeline-ns2.yaml
kubectl apply -f pipeline-ns1.yaml 
kubectl apply -f pipeline-ns2.yaml 
```

Now create the RoleBinding for the `view` role

```sh
k create clusterrolebinding pipeline-rb-ns2 --serviceaccount ns2:pipeline --clusterrole=view $DO > pipeline-rb-view-ns2.yaml
k create clusterrolebinding pipeline-rb-ns1 --serviceaccount ns1:pipeline --clusterrole=view $DO > pipeline-rb-view-ns1.yaml
k apply -f pipeline-rb-view-ns1.yaml
k apply -f pipeline-rb-view-ns2.yaml
```

Now create a ClusterRole for create/delete in their namespaces:

```sh
k create clusterrole pipeline-create-delete -n ns1 --verb=create,delete --resource=deployments $DO > pipeline-create-delete.yaml
k apply -f pipeline-create-delete.yaml
```

Now a RoleBinding for the namespaces:

```sh
k create rolebinding pipeline-create-rb-ns1 -n ns1 --clusterrole pipeline-create-delete --serviceaccount ns1:pipeline $DO > pipeline-create-rb-ns1.yaml
k create rolebinding pipeline-create-rb-ns1 -n ns2 --clusterrole pipeline-create-delete --serviceaccount ns2:pipeline $DO > pipeline-create-rb-ns2.yaml
```

Then all of these should work:

```sh
# namespace ns1 deployment manager
k auth can-i delete deployments --as system:serviceaccount:ns1:pipeline -n ns1 # YES
k auth can-i create deployments --as system:serviceaccount:ns1:pipeline -n ns1 # YES
k auth can-i update deployments --as system:serviceaccount:ns1:pipeline -n ns1 # NO
k auth can-i update deployments --as system:serviceaccount:ns1:pipeline -n default # NO

# namespace ns2 deployment manager
k auth can-i delete deployments --as system:serviceaccount:ns2:pipeline -n ns2 # YES
k auth can-i create deployments --as system:serviceaccount:ns2:pipeline -n ns2 # YES
k auth can-i update deployments --as system:serviceaccount:ns2:pipeline -n ns2 # NO
k auth can-i update deployments --as system:serviceaccount:ns2:pipeline -n default # NO

# cluster wide view role
k auth can-i list deployments --as system:serviceaccount:ns1:pipeline -n ns1 # YES
k auth can-i list deployments --as system:serviceaccount:ns1:pipeline -A # YES
k auth can-i list pods --as system:serviceaccount:ns1:pipeline -A # YES
k auth can-i list pods --as system:serviceaccount:ns2:pipeline -A # YES
k auth can-i list secrets --as system:serviceaccount:ns2:pipeline -A # NO (default view-role doesn't allow)
```

# User / Role / RoleBindings

There is existing Namespace `applications` .

User `smoke` should be allowed to `create` and `delete` `Pods, Deployments and StatefulSets` in Namespace `applications`.
User `smoke` should have view permissions (like the permissions of the default ClusterRole named view ) in all Namespaces but not in `kube-system` .
Verify everything using `kubectl auth can-i` .

Verify all namespaces:

```sh
$ k get ns
NAME              STATUS   AGE
applications      Active   2m22s
default           Active   2d3h
kube-node-lease   Active   2d3h
kube-public       Active   2d3h
kube-system       Active   2d3h
```

First change to the namespace: 

```sh
$ kn applications
Context "kubernetes-admin@kubernetes" modified.
```

Now create a role and role binding for editing

```sh
kubectl create role $DO smoke-edit -n applications --verb=create,delete --resource=deployments,statefulsets,pods > smoke-edit-role.yaml
kubectl create rolebinding $DO smoke-edit-rb -n applications --user smoke --role smoke-edit > smoke-edit-rb.yaml
```

And then create the rolebinding for the ClusterRole view and append the other role bindings:

```sh
$ k create rolebinding $DO smoke-view-app-rb -n applications --clusterrole view --user smoke > smoke-view.yaml
$ create rolebinding $DO smoke-view-default-rb -n default --clusterrole view --user smoke >> smoke-view.yaml
$ k create rolebinding $DO smoke-view-kp-rb -n kube-public --clusterrole view --user smoke >> smoke-view.yaml
$ k create rolebinding $DO smoke-view-knl-rb -n kube-node-lease --clusterrole view --user smoke >> smoke-view.yaml

# Add yaml seperators in the file and apply it
$ kubectl apply -f smoke-view.yaml
rolebinding.rbac.authorization.k8s.io/smoke-view-app-rb configured
rolebinding.rbac.authorization.k8s.io/smoke-view-default-rb configured
rolebinding.rbac.authorization.k8s.io/smoke-view-kp-rb configured
rolebinding.rbac.authorization.k8s.io/smoke-view-knl-rb created
```

Now run some tests:

```sh
# applications
k auth can-i create deployments --as smoke -n applications # YES
k auth can-i delete deployments --as smoke -n applications # YES
k auth can-i delete pods --as smoke -n applications # YES
k auth can-i delete sts --as smoke -n applications # YES
k auth can-i delete secrets --as smoke -n applications # NO
k auth can-i list deployments --as smoke -n applications # YES
k auth can-i list secrets --as smoke -n applications # NO
k auth can-i get secrets --as smoke -n applications # NO

# view in all namespaces but not kube-system
k auth can-i list pods --as smoke -n default # YES
k auth can-i list pods --as smoke -n applications # YES
k auth can-i list pods --as smoke -n kube-public # YES
k auth can-i list pods --as smoke -n kube-node-lease # YES
k auth can-i list pods --as smoke -n kube-system # NO
```


# Scheduler Priority

Find the Pod with the highest priority in Namespace `management` and delete it.

```sh
kubectl get pod -n management
```

```sh
$ kgp -n management -o=custom-columns="NAME:.metadata.name,PRIORITY:.spec.priority"
NAME       PRIORITY
runner     200000000
sprinter   300000000

$ k delete pod -n management sprinter --grace-period=0 --force
pod "sprinter" deleted
```

In Namespace `lion` there is one existing Pod which requests `1Gi` of memory resources. That Pod has a specific priority because of its PriorityClass. Create new Pod named important of image `nginx:1.21.6-alpine` in the same Namespace. It should request `1Gi` memory resources Assign a higher priority to the new Pod so it's scheduled instead of the existing one.

Both Pods won't fit in the cluster.

```sh
$ k get pod 4d37006c -o yaml | grep priority
  priority: 200000000
  priorityClassName: level2

 $ k get priorityclass        
NAME                      VALUE        GLOBAL-DEFAULT   AGE
level2                    200000000    false            10m
level3                    300000000    false            10m
system-cluster-critical   2000000000   false            2d3h
system-node-critical      2000001000   false            2d3h
```

Use a priority class of `level3` instead of `level2`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: important
  namespace: lion
spec:
  containers:
  - image: nginx:1.21.6-alpine
    name: nginx
    resources:
      requests:
        memory: 1Gi
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  priorityClassName: level3
```

```sh
$ kaf important.yaml 
pod/important created

 $ k get pod
NAME        READY   STATUS    RESTARTS   AGE
important   1/1     Running   0          3s
```