# Securing the Supply Chain

For software products there are a lot of products that are used to get the end result

- Development Tools
- Containers
- CI/CD Registry
- Kubernetes in the Cloud
- Web Browser

There could be security vulnerabilities anywhere throughout there. Developers can control the following:

- Containers
- CI/CD Registry
- Kubernetes in the Cloud

List all images in your cluster

```sh
kubectl get pods -A -o='custom-columns=:spec.containers[*].image' | sort | uniq'
```

Outputs:

```
busybox
docker.io/calico/cni:v3.24.1
docker.io/calico/kube-controllers:v3.24.1
docker.io/calico/node:v3.24.1
docker.io/kubernetesui/dashboard-api:1.7.0
docker.io/kubernetesui/dashboard-auth:1.1.3
docker.io/kubernetesui/dashboard-metrics-scraper:1.1.1
docker.io/kubernetesui/dashboard-web:1.4.0
docker.io/library/busybox:latest
docker.io/library/kong:3.6
docker.io/openpolicyagent/gatekeeper:v3.5.2
kong:3.6
openpolicyagent/gatekeeper:v3.5.2
quay.io/coreos/flannel:v0.15.1
registry.k8s.io/coredns/coredns:v1.11.1
registry.k8s.io/etcd:3.5.12-0
registry.k8s.io/kube-apiserver:v1.29.6
registry.k8s.io/kube-controller-manager:v1.29.6
registry.k8s.io/kube-proxy:v1.29.6
registry.k8s.io/kube-scheduler:v1.29.6
```

Another way to see it by how it is assigned to a pod

```sh
$ kubectl get pods -n ns -o='custom-columns=NAME:metadata.name,IMAGE:spec.containers[*].image' -A
NAME                             IMAGE
cassandra                        nginx
accessor                         nginx
backend                          nginx
frontend                         nginx
coredns-668d6bf9bc-dnp8p         registry.k8s.io/coredns/coredns:v1.11.3
coredns-668d6bf9bc-vkft6         registry.k8s.io/coredns/coredns:v1.11.3
etcd-master                      registry.k8s.io/etcd:3.5.16-0
kube-apiserver-master            registry.k8s.io/kube-apiserver:v1.32.6
kube-controller-manager-master   registry.k8s.io/kube-controller-manager:v1.32.6
kube-proxy-bj69n                 registry.k8s.io/kube-proxy:v1.32.6
kube-proxy-m87mr                 registry.k8s.io/kube-proxy:v1.32.6
kube-scheduler-master            registry.k8s.io/kube-scheduler:v1.32.6
weave-net-dmwrc                  weaveworks/weave-kube:latest,weaveworks/weave-npc:latest
weave-net-k95lj                  weaveworks/weave-kube:latest,weaveworks/weave-npc:latest
```

# Trusted Images with OPA

Whitelist some registries using OPA:

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8strustedimages
spec:
  crd:
    spec:
      names:
        kind: K8sTrustedImages
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8strustedimages

        violation[{"msg": msg}] {
          image := input.review.object.spec.containers[_].image
          not startswith(image, "docker.io/")
          not startswith(image, "openpolicyagent/")
          not startswith(image, "quay.io/")
          not startswith(image, "registry.k8s.io/")
          msg := "not trusted image!"
        }
```


```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sTrustedImages
metadata:
  name: pod-trusted-images
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
```

This fails:

```sh
$ kubectl run nginx --image nginx
Error from server ([pod-trusted-images] not trusted image!): admission webhook "validation.gatekeeper.sh" denied the request: [pod-trusted-images] not trusted image!
```

This succeeds:

```sh
$ kubectl run nginx --image docker.io/nginx
pod/nginx created
```

## ImagePolicyWebhook

You can use an external service (webhook) using the ImagePolicyWebhook Admission controller. You can see how to set one up to an external service here:

https://youtu.be/d9xfB5qaOfg?t=30102

The idea is the Admission Controller conacts the external service with the list of containers in a `ImageReview` object. The service returns if the are useable or not. You can write the external service in whatever language you choose.

Add an `ImagePolicyWebhook` to the `--enable-admission-plugins`:

```yaml
 - --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
 - --admission-control-config-file=/etc/kubernetes/admission/admission_config.yaml
```

It will fail as there is no configuration for that. You need an `AdmissionConfiguration` in an `admission_config.yaml`:

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
  - name: ImagePolicyWebhook
    configuration:
      imagePolicy:
        kubeConfigFile: /etc/kubernetes/admission/kubeconf
        allowTTL: 50
        denyTTL: 50
        retryBackoff: 500
        defaultAllow: true
```

`defaultAllow` allows new pods to work even if the external service is done. The `kubeconf` is used to contact the external service with certifications

```yaml
apiVersion: v1
kind: Config

# clusters refers to the remote service.
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/admission/external-cert.pem  # CA for verifying the remote service.
    server: https://external-service:1234/check-image                   # URL of remote service to query. Must use 'https'.
  name: image-checker

contexts:
- context:
    cluster: image-checker
    user: api-server
  name: image-checker
current-context: image-checker
preferences: {}

# users refers to the API server's webhook configuration.
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/admission/apiserver-client-cert.pem     # cert for the webhook admission controller to use
    client-key:  /etc/kubernetes/admission/apiserver-client-key.pem             # key matching the cert
```

After you add the following to the API server, you must also mount the `/etc/kubernetes/admission` folder

```yaml
 - --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
 - --admission-control-config-file=/etc/kubernetes/admission/admission_config.yaml
```


The API server can not start because the service is down:

```sh
$ k run test-nginx --image nginx
Error from server (Forbidden): pods "test-nginx" is forbidden: Post "https://external-service:1234/check-image?timeout=30s": dial tcp lookup external-service on 169.254.169.254.53: no such host
```

If the `defaultAllow: true` is set in the `AdmissionConfiguration` than you no longer get that error. You must restart the Kubernetes API Server.
