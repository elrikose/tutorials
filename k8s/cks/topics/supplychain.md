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
kubectl get pods -A -oyaml | grep "image:" | sort | uniq | awk '{print $2}'
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

You can use an external webhook using the ImagePolicyWebhook Admission controller. You can see how to set one up to an external service here:

https://youtu.be/d9xfB5qaOfg?t=30102