# Security Contexts

Allow for the definition of privilege and access control for a pod OR container

https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

- define user ID and group ID
- Privileged or Unprivileged
- Linux system calls

```yaml
spec:
  securityContext:   # Pod Level
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
    ...
    securityContext:  # Container Level
      runAsUser: 5000 # override the pod user
```

So create a pod

```sh
kubectl run security-context-pod --image busybox -oyaml --dry-run=client -- sh -c "sleep 1d" > security-context-pod.yaml
```

And then add the `securityContext:` at the pod level:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 2000
    fsGroup: 3000
  containers:
  - args:
    - sh
    - -c
    - sleep 1d
    image: busybox
    name: security-context-pod
```

Then create it and then see how it is being run

```sh
$ kubectl apply -f security-pod-context.yaml
$ kubectl exec security-context-pod -it -- sh
~ $ id
uid=1000 gid=2000 groups=3000
```

At the container level you can also for running as non root and it will error if you don't specify one in the container

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: security-context-pod
  name: security-context-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 2000
    fsGroup: 3000
  containers:
  - args:
    - sh
    - -c
    - sleep 1d
    image: busybox
...
    securityContext:
      runAsNonRoot: true
```

# Privileged Containers

Containers run unprivileged by default. If you pass `--privileged` to the container runtime then the host's root 0 is the same as the containers root.

In Kubernetes you can allow a pod to run privileged by using a security context:

```yaml
spec:
  securityContext:
    privileged: true
```

There is also an ability for a pod to gain more privilege, which Kubernetes sets to default. Typically you disable it:

```yaml
spec:
  securityContext:
    allowPrivilegeEscalation: false
```
