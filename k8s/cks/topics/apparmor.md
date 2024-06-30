# AppArmor

AppArmor - Shield between app and the kernel level functions.

https://kubernetes.io/docs/tutorials/security/apparmor/

>AppArmor is applied to a Pod by specifying an AppArmor profile that each container should be run with. If any of the specified profiles are not loaded in the kernel, the kubelet will reject the Pod. You can view which profiles are loaded on a node by checking the /sys/kernel/security/apparmor/profiles file. 

A profile is created to restrict what an app can do. Three profile modes:

- Unconfined - nothing enforced
- Complain - process can run, but issues will be logged
- Enforce - process won't be able to run if against profile

Install so management utilities:

```sh
sudo apt install apparmor-utils
```

And the commands you can run most often:

```sh
# Show status of all profiles AppArmor knows about
aa-status
apparmor_status

# Generate a new profile
aa-genprof

# Put a profile in complain mode
aa-complain

# Put profile in enforce mode
aa-enforce

# Re-read the log and allow certain items
aa-logprof
```

You can see if the service is running with:

```sh
$ sudo systemctl status apparmor.service
● apparmor.service - Load AppArmor profiles
     Loaded: loaded (/lib/systemd/system/apparmor.service; enabled; vendor preset: enabled)
     Active: active (exited) since Sat 2024-06-29 11:15:27 EDT; 1 day 5h ago
       Docs: man:apparmor(7)
             https://gitlab.com/apparmor/apparmor/wikis/home/
   Main PID: 537 (code=exited, status=0/SUCCESS)
      Tasks: 0 (limit: 4655)
     Memory: 0B
     CGroup: /system.slice/apparmor.service

Jun 29 11:15:27 worker systemd[1]: Starting Load AppArmor profiles...
Jun 29 11:15:27 worker apparmor.systemd[537]: Restarting AppArmor
Jun 29 11:15:27 worker apparmor.systemd[537]: Reloading AppArmor profiles
Jun 29 11:15:27 worker apparmor.systemd[556]: Skipping profile in /etc/apparmor.d/disable: usr.sbin.rsyslogd
Jun 29 11:15:27 worker systemd[1]: Finished Load AppArmor profiles.
```

You add a profile with

```sh
apparmor_parser <profilefile>
```

You can get the status of the profile with either of these two commands:

```sh
aa-status

apparmor_status
```

And then grep for a certain profile type

```sh
$ sudo aa-status | grep docker
   docker-default
```

Before v1.30, You have to set the AppArmor profile in a deployment's template annotation section, not the deployment section:

```yaml
  template:
    metadata:
      annotations:
        container.apparmor.security.beta.kubernetes.io/httpd: localhost/docker-default
```
Like so:

```sh
$ k get deploy spacecow -n moon -oyaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "2"
  name: spacecow
  namespace: moon
spec:
  replicas: 3
  selector:
    matchLabels:
      app: spacecow
  template:
    metadata:
      annotations:
        container.apparmor.security.beta.kubernetes.io/httpd: localhost/docker-default
      creationTimestamp: null
      labels:
        app: spacecow
    spec:
      containers:
      - image: httpd:2.4.52-alpine
        imagePullPolicy: IfNotPresent
        name: httpd
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
```

After v1.30, you do it as part of the securityContext at either the pod or container level like so:

```yaml
securityContext:
  appArmorProfile:
    type: <profile_type>
```

Where the type is one of 3 things
- RuntimeDefault to use the runtime's default profile
- Localhost to use a profile loaded on the host (see below)
- Unconfined to run without AppArmor

```yaml
securityContext:
  appArmorProfile:
    type: Localhost
    localhostProfile: k8s-apparmor-example-deny-write
```

# Exercise: Create a profile for curl

Log into worker node and curl something:

```sh
$ curl -v github.com
*   Trying 140.82.114.4:80...
* TCP_NODELAY set
* Connected to github.com (140.82.114.4) port 80 (#0)
> GET / HTTP/1.1
> Host: github.com
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 301 Moved Permanently
< Content-Length: 0
< Location: https://github.com/
< 
* Connection #0 to host github.com left intact
```

Create a profile for `curl`:

```sh
aa-genprof curl
```

If you choose `S` that scans the event logs for what it can do.
If you choose `F` that limits all actions in the profile

Selected `F`:

```sh
$ curl -v github.com
* Could not resolve host: github.com
* Closing connection 0
curl: (6) Could not resolve host: github.com
```

Here is the profile that was created:

```sh
$ cat /etc/apparmor.d/usr.bin.curl 
# Last Modified: Sun Jun 30 16:39:34 2024
#include <tunables/global>

/usr/bin/curl {
  #include <abstractions/base>

  /usr/bin/curl mr,

}
```

Now you can re-allow `curl` to work by using the `aa-logprof` command:

```sh
$ aa-logprof 
Reading log entries from /var/log/syslog.
Updating AppArmor profiles in /etc/apparmor.d.
Enforce-mode changes:

Profile:  /usr/bin/curl
Path:     /etc/ssl/openssl.cnf
New Mode: owner r
Severity: 2

 [1 - #include <abstractions/openssl>]
  2 - #include <abstractions/ssl_keys> 
  3 - owner /etc/ssl/openssl.cnf r, 
(A)llow / [(D)eny] / (I)gnore / (G)lob / Glob with (E)xtension / (N)ew / Audi(t) / (O)wner permissions off / Abo(r)t / (F)inish
```

Allow the command with `A`. and then save with `S`:

The profile looks like this:

```sh
$ cat /etc/apparmor.d/usr.bin.curl 
# Last Modified: Sun Jun 30 16:46:08 2024
#include <tunables/global>

/usr/bin/curl {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  #include <abstractions/openssl>

  /usr/bin/curl mr,

```

And `curl` works:

```sh
$ curl -v github.com
*   Trying 140.82.114.3:80...
...
* Mark bundle as not supporting multiuse
< HTTP/1.1 301 Moved Permanently
< Content-Length: 0
< Location: https://github.com/
```

# Exercise: Nginx container uses AppArmor profile

Grab the app armor profile from here:

https://github.com/killer-sh/cks-course-environment/blob/master/course-content/system-hardening/kernel-hardening-tools/apparmor/profile-docker-nginx

```sh
cd /etc/apparmor.d
curl https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/course-content/system-hardening/kernel-hardening-tools/apparmor/profile-docker-nginx > docker-nginx
```

And then add it via apparmor_parser:

```sh
$ sudo apparmor_parser ./docker-nginx
$ sudo aa-status | grep docker-nginx
   docker-nginx
```

Then when you launch it from docker/podman you can specify a security option to run it via the `--security-opt` option:

```sh
$ podman run --security-opt apparmor=docker-default nginx
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/06/30 21:13:49 [notice] 1#1: using the "epoll" event method
2024/06/30 21:13:49 [notice] 1#1: nginx/1.27.0
2024/06/30 21:13:49 [notice] 1#1: start worker process 25
```

And then you can run it with the new profile:

```sh
$ podman run -d --security-opt apparmor=docker-nginx nginx
/docker-entrypoint.sh: 13: cannot create /dev/null: Permission denied
/docker-entrypoint.sh: No files found in /docker-entrypoint.d/, skipping configuration
2024/06/30 21:15:39 [notice] 1#1: using the "epoll" event method
2024/06/30 21:15:39 [notice] 1#1: nginx/1.27.0
2024/06/30 21:15:39 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2024/06/30 21:15:39 [notice] 1#1: OS: Linux 5.4.0-187-generic
2024/06/30 21:15:39 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/06/30 21:15:39 [notice] 1#1: start worker processes
2024/06/30 21:15:39 [notice] 1#1: start worker process 4
2024/06/30 21:15:39 [notice] 1#1: start worker process 5
```

There is an error with `/dev/null`

But then you can exec into the container and it is a bit more locked down:

```sh
$ podman run -d --security-opt apparmor=docker-nginx nginx
b6fe83fa99f977460a3448cb69edf4dc420ad3f6b4fdaa4efb319072a716e183
root@worker:/etc/apparmor.d# podman exec -it b6fe83fa99f977460a3448cb69edf4dc420ad3f6b4fdaa4efb319072a716e183 sh
$ touch /root/test
touch: cannot touch '/root/test': Permission denied
```

# Exercise: Nginx pod uses AppArmor profile

- App Armor need to be installed on every node
- Profile has to be available on every node
- Profiles are specified by container by container
- Add it to manifest via annotation

Annotation spec is here:

```yaml
annotations:
  container.apparmor.security.beta.kubernetes.io/secure-nginx: localhost/docker-nginx
```

In K8s 1.30 you use a new `securityContext:` called `appArmorProfile:`.

Create a new `secure-nginx` pod:

```sh
kubectl run secure-nginx --image=nginx:1.27 -oyaml --dry-run=client > secure-nginx.yaml
```

And then add the annotation with a profile that doesn't exist:

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  annotations:
    container.apparmor.security.beta.kubernetes.io/secure-nginx: localhost/hello
  labels:
    run: secure-nginx
  name: secure-nginx
spec:
  containers:
  - image: nginx:1.27
    name: secure-nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

It fails with the following error:

```sh
  Warning  Failed     5s (x5 over 28s)  kubelet            Error: failed to get container spec opts: failed to generate apparmor spec opts: apparmor profile not found hello
```

Then change the annotation back to the following:

```yaml
  annotations:
    container.apparmor.security.beta.kubernetes.io/secure-nginx: localhost/docker-nginx
```

And it succeeds.



