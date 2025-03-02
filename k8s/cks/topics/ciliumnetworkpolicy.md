# CiliumNetworkPolicy

Within the last year, there has been more

# Level 3 Policies

Layer 3 network policies that connect at the OSI layer 3:
- Services/CIDRs
- Endpoints (IP addresses) - uses label selectors not IP addresses
- Entities

[Layer 3 Examples](https://docs.cilium.io/en/latest/security/policy/language/)

Deny all access:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "deny-all-egress"
spec:
  endpointSelector:
    matchLabels:
      role: restricted
  egress:
  - {}
```

Allow all access:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "allow-all"
spec:
  endpointSelector:
    matchLabels:
      role: frontend
  ingress:
  - fromEndpoints:
    - {}
```

The backend only allows access from the frontend:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "from-frontend"
spec:
  endpointSelector:
    matchLabels:
      role: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        role: frontend
```

The frontend can only communicated with the backend:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "to-backend"
spec:
  endpointSelector:
    matchLabels:
      role: frontend
  egress:
  - toEndpoints:
    - matchLabels:
        role: backend
```

# Layer 4 Policies

You get to navigate to specific ports

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "layer4-rule"
spec:
  endpointSelector:
    matchLabels:
      app: myService
  egress:
    - toPorts:
      - ports:
        - port: "80"
          protocol: TCP
```

And CIDRs with ports:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "cidr-layer4-rule"
spec:
  endpointSelector:
    matchLabels:
      role: crawler
  egress:
  - toCIDR:
    - 192.0.2.0/24
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
```

# Layer 7 Policies

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "rule1"
spec:
  description: "Allow HTTP GET /public from env=prod to app=service"
  endpointSelector:
    matchLabels:
      app: service
  ingress:
  - fromEndpoints:
    - matchLabels:
        env: prod
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/public"
```

# Reference

[Overview of Network Policy](https://docs.cilium.io/en/latest/security/policy/)
