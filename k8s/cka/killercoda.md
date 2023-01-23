# Killer Coda Simulator and Scenarios

The [Killer Coda](https://killercoda.com/killer-shell-cka) CKA simulator has scenarios to help with testing the CKA.

# API Server Crash

Use the following debug if the K8s API Server or other components have crashed. Often when the API server has crashed you have to drop back out to the container runtime. In this cake is 

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

The api server will fail on the following, but I

f the controller manager or etcd is down, you will get a CrashLoopBackOff:

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

# User / Role / RoleBindings

# Scheduler Priority