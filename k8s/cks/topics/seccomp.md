# seccomp

seccomp - Secure Computing mode

- Security mechanism in Linux Kernel
- Restricts execution of syscalls
  - read()
  - write()
  - exec()
  - getpid()

Prevent calling `exec()` or `getpid()` by killing the process.

Nowadays, seccomp is combined with BPF filters (aka seccomp-bpf)

# Exercise: Install seccomp profile

One from the course:

https://github.com/killer-sh/cks-course-environment/blob/master/course-content/system-hardening/kernel-hardening-tools/seccomp/profile-docker-nginx.json

Install it on the worker node:

```sh
curl -O https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/course-content/system-hardening/kernel-hardening-tools/seccomp/profile-docker-nginx.json
```

# Exercise: Create a Nginx container in Docker

Then just like AppArmor you can specify running it via the `--security-opt` command-line option

```sh
$ docker run --security-opt seccomp=profile-docker-nginx.json nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
2cc3ae149d28: Pull complete 
...
2024/06/30 21:44:41 [notice] 1#1: start worker processes
2024/06/30 21:44:41 [notice] 1#1: start worker process 29
2024/06/30 21:44:41 [notice] 1#1: start worker process 30
```

Now change the profile and remove the `write` function and re-run:

```sh
$ sudo docker run --security-opt seccomp=profile-docker-nginx.json nginx
docker: Error response from daemon: OCI runtime start failed: cannot start an already running container: unknown.
ERRO[0000] error waiting for container: 
```

# Exercise: Create a Nginx pod

For Kubernetes we need to put it somewhere where the kubelet can see it. Documentation (kubelet seccomp):

https://kubernetes.io/docs/tutorials/security/seccomp/

There is an argument that can be passed to the kubelet `--seccomp-profile-root` which usually defaults to `/var/lib/kubelet/seccomp`. Then you copy the profile in:

```sh
mkdir /var/lib/kubelet/seccomp
cp ~ubuntu/profile-docker-nginx.json .
```

Then you create a pod with the security context:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secure-nginx
  name: secure-nginx
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profile-docker-nginx.json
  containers:
  - image: nginx:1.27
    name: secure-nginx
    resour ces: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```


If you put the wrong file name in there it fails:

```sh
  Warning  Failed     11s (x4 over 25s)  kubelet            Error: failed to create containerd container: cannot load seccomp profile "/var/lib/kubelet/seccomp/docker-nginx.json": open /var/lib/kubelet/seccomp/docker-nginx.json: no such file or directory
```

