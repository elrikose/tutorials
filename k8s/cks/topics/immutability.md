# Container Immutability

Immutability - container won't be modified in its lifetime
- Prevent a user from getting access on a container and changing what it does or the service.
- We always know the state of the application because a mutable would be changed from intial start

Why Immutable?
- Advanced deployment methods
- Easy Rollback
- More reliability
- Better container level security

How?
- Remove shells
- Make filesystem read-only
- Don't run as root

Ways in which to do this in Kubernetes?
- Run a command to set the permissions of root folder (hacky)
- A startupProbe can run to set permissions too (hacky)
- Use SecurityContexts
  - enforce read only file systems
  - enforce not run as root
- Use initContainer to setup the container with read-write. main container can only read with volume mount.

# Exercise: Use Startup Probe to remove touch and bash

```sh
kubectl run immutable --image=httpd -oyaml --dry-run=client
```

And then you delete `touch` and `bash` after the fact.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: immutable
spec:
  containers:
  - image: httpd
    name: immutable
    resources: {}
    startupProbe:
      exec:
        command:
        - rm
        - /bin/touch
        - /bin/bash
      initialDelaySeconds: 1
      periodSeconds: 5
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```

# Exercise: Make Read-only file system add emptyDir for certain volumes

```sh
kubectl run immutable --image=httpd -oyaml --dry-run=client
```

- Set the `securityContext:` to `readOnlyRootFilesystem: true`
- Add an `emptyDir:` for the logs

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: immutable
spec:
  containers:
  - image: httpd
    name: immutable
    resources: {}
    securityContext:
      readOnlyRootFilesystem: true
    volumeMounts:
    - mountPath: /usr/local/apache2/logs
      name: log-volume
  volumes:
  - name: log-volume
    emptyDir: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```
