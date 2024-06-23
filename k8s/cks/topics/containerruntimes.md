# Container Runtime Sandboxes

"Containers are not contained" - Just because it is in a container doesn't mean it is more protected

Containers are running in their own Kernel Group, but that doesn't mean it can't get out of it.

Sandbox
- Additional security layer to reduce attack surface
- System calls get a sandbox layer that limits directly calling the System Calls
- Sandboxes are not free because of the layer
- Not good for a lot of system calls
- No ability to communicate directly to hardware

# Open Container Initiative (OCI)

Open Container Initiative is a Linux Foundation initiative to create standards for virtualization. There is a spec for:

- runtime
- image
- distribution

OCI creates a runtime called `runc`. 

# Container Runtime Interface

Kubelets can talk to multiple container runtimes:

- dockershim --> dockerd --> containerd --> runc
- containderd --> shim API --> Kata / Firecracker / gVisor
- cri-o --> runc

Kata, Firecracker, and gVisor are container runtime sandboxes.

`--container-runtime` is used at the kubelet to decide what container runtime to use. It can't use more than 1.

## Kata Containers

Kata containers uses a lightweight VM to isolate the images into their own Kernel

- Strong separation layer
- Every container is in its own private VM
- QEMU is used by default

## gVisor

gVisor is from Google -- A user spacee kernel for containers
- Again separation
- Not Hypervisor or VM based
- Simulates kernel calls 
- Runtime is called `runsc`

gVisor uses a `RuntimeClass`

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

And then deploy it:

```sh
$ kubectl apply -f gvisor-rc.yaml 
runtimeclass.node.k8s.io/gvisor created
```

Create a dummy runtime class called test:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  name: gvisor
spec:
  runtimeClassName: test
  containers:
...
```

It will get a problem because the `test` runtime class doesn't exist

```sh
$ kubectl apply -f gvisor.yaml                                    
Error from server (Forbidden): error when creating "gvisor.yaml": pods "gvisor" is forbidden: pod rejected: RuntimeClass "test" not found
```

Now change it to gvisor:

```sh
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: gvisor
  name: gvisor
spec:
  runtimeClassName: test
  containers:
  - image: nginx
    name: gvisor
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

The pod starts, but fails at container creating step:

```sh
$ kubectl describe pod gvisor
...
  Warning  FailedCreatePodSandBox  5s (x2 over 16s)  kubelet            Failed to create pod sandbox: rpc error: code = Unknown desc = failed to get sandbox runtime: no runtime for "runsc" is configured
```

Now you have to install runsc by logging into your worker node. Here is an Ubuntu script that will do it:

https://github.com/killer-sh/cks-course-environment/blob/master/course-content/microservice-vulnerabilities/container-runtimes/gvisor/install_gvisor.sh

After you install the `kubelet` and `containerd` should be running. Then you should see that the pod should be running in a gvisor sandbox

```sh
$ kubectl exec gvisor -it -- bash             
root@gvisor:/# uname -a
Linux gvisor 4.4.0 #1 SMP Sun Jan 10 15:06:54 PST 2016 x86_64 GNU/Linux
```




