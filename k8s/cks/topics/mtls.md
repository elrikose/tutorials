# Mutual TLS

Kubernetes traffic is unencrypted by default. Mutual TLS (mTLS) is to use certificates to encrypt traffic two-way.

You can encrypt the traffic by a service mesh:
- Proxy sidecar for each container. 
- Certs are maintained by service mesh.
- initContainer sets up network routing through the proxy

Service Meshs:
- istio
- linkerd

Create a `mutual-tls` pod:

```sh
kubectl run mutual-tls --image=bash -oyaml --dry-run=client -- sh -c 'ping google.com' > mutual-tls.yaml
```

This is the manifest:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mutual-tls
spec:
  containers:
  - args:
    - sh
    - -c
    - ping google.com
    image: bash
    name: mutual-tls
    resources: {}
```

Then you add a proxy:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mutual-tls
spec:
  containers:
 ...
   - args:
    - sh
    - -c
    - 'apt update && apt install iptables -y && iptables -L && sleep 1d'
    image: ubuntu
    name: proxy
    resources: {}
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mutual-tls
spec:
  containers:
...
  - args:
    - sh
    - -c
    - 'apt update && apt install iptables -y && iptables -L && sleep 1d'
    image: ubuntu
    name: proxy
    resources: {}
    securityContext:
      capabilities:
        add: ["NET_ADMIN"]
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

