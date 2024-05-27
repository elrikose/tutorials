# AppArmor

https://kubernetes.io/docs/tutorials/security/apparmor/

>AppArmor is applied to a Pod by specifying an AppArmor profile that each container should be run with. If any of the specified profiles are not loaded in the kernel, the kubelet will reject the Pod. You can view which profiles are loaded on a node by checking the /sys/kernel/security/apparmor/profiles file. 

You can see if the service is running with:

```sh
sudo systemctl status apparmor.service
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
aa-status | grep docker
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
