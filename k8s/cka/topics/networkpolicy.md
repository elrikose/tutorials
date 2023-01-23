# NetworkPolicy

This is a good reference for understanding Network Policies in Kubernetes:

https://www.youtube.com/watch?v=u1KUft3fsCk

NetworkPolicy controls traffic to and from a pod or a group of pods using a selector.

There are 2 types of policies:

- Ingress - incoming to pod/pod group
- Egress - outgoing from pod/pod group

Ingress or Egress can be controlled by one of these three types

- ipBlock
- namespaceSelector
- podSelector

## Allowing Examples

Allow All Ingress:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  ingress:
  - {}
  policyTypes:
  - Ingress
```

Allow all Egress:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
spec:
  podSelector: {}
  egress:
  - {}
  policyTypes:
  - Egress
```


## Denying All Ingress and Egress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

