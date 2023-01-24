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



# Scheduler Priority