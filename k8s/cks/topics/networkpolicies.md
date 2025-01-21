# Network Policies

They are namespace scoped firewall Rules in Kubernetes. Restrict Ingress and Egress for pods based on rules/conditions.

Only implemented by network plugins:
- Calico
- Weave

If you don't have the network plugins, the resources are just ignored. By default every pod is not isolated and can communicate with every other pod.

# Policy Examples

Allow all traffic to the backend pods

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-allow-all
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - {}
```

The `{}` is an empty selector and selects ALL items. The null selector `[]` selects no items.

Default Deny of everything in the default namespace.

```yaml
# deny all incoming and outgoing traffic from all pods in namespace default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
```

The `podSelector: {}` is an empty selector and selects ALL items. A null selector `[]` selects no items.

Default deny of everything except DNS (port 53):

```yaml
# deny all incoming and outgoing traffic from all pods in namespace default
# but allow DNS traffic. This way you can do for example: kubectl exec frontend -- curl backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
  egress:
  - ports:
    - port: 53
      protocol: TCP
    - port: 53
      protocol: UDP
```

# Scenario - Create Default Deny from Frontend and Backend

Launch a mock frontend and backend pod

```sh
kubectl run frontend --image nginx
kubectl run backend --image nginx
```

Then expose them as services

```sh
kubectl expose pod frontend --port 80
kubectl expose pod backend --port 80
```

Then test connectivity

```sh
kubectl exec frontend -- curl backend
kubectl exec backend -- curl frontend
```

Then create a network policy

```sh
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
```

For DNS resolution you should change the default-deny to include port 53:

```sh
# deny all incoming and outgoing traffic from all pods in namespace default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
  egress:
  - to:
    ports:
    - port: 53
      protocol: TCP
    - port: 53
      protocol: UDP
```


# Scenario - Allow Egress from Frontend to Backend

Egress from backend

```sh
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-allow
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: frontend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          run: backend
```


Ingress into the backend

```sh
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-allow
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          run: frontend
```

# Scenario - Now Allow Access to Cassandra in a different namespace

Add a new namespace `cassandra`

```sh
kubectl create ns cassandra
```

Add the labels `ns: cassandra` to the namespaces `labels:` section.

Simulate starting cassandra with `nginx` and expose it

```sh
kubectl run cassandra -n cassandra --image nginx
kubectl expose pod cassandra -n cassandra --port 80
```

Change the `backend` Network Policy to include egress:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-allow
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          run: frontend
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          ns: cassandra
```

Add deny cassandra:

```yaml
# deny all incoming and outgoing traffic from all pods in namespace cassandra
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: cassandra
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
  egress:
  - to:
    ports:
    - port: 53
      protocol: TCP
    - port: 53
      protocol: UDP
```

And then allow from the default namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cassandra-allow
  namespace: cassandra
spec:
  podSelector:
    matchLabels:
      run: cassandra
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: default
```

# Preventing Pod access to Metadata

Block egress to the metadata server at `169.254.169.254/32` by default:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cloud-metadata-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32
```

But some pods need access to the metadata server:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cloud-metadata-allow
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: metadata-accessor
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 169.254.169.254/32
```
