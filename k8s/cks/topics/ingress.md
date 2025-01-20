# Ingress

What is Ingress?

There are many different types of Ingress controllers.

The most popular is a pod with nginx in it. The Kubernetes manifest wraps around nginx so that you don't have to edit Nginx configuration files.

Ingress requires a LoadBalancer. LoadBalancer requires a NodePart service that requires a ClusterIP service.

# Setting up Ingress without TLS

Create some pods and expose some services:

```sh
# Create the pods
kubectl run pod1 --image nginx
kubectl run pod2 --image httpd

# Expose the services
kubectl expose pod pod1 --port 80
kubectl expose pod pod2 --port 80
```

Create the ingress. Notice there is no `host:` because we are just using an IP

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx # newer Nginx-Ingress versions NEED THIS
  rules:
  - http:
      paths:
      - path: /service1
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80

      - path: /service2
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 80
```


# Setting up Ingress with TLS

Create a self-signed certificate. Set the "Common Name" to the domain (eg. "mydomain.com")

```sh
openssl req -x509 -newkey rsa:4096 -keyout tls.pem -out tls.crt -days 365 -nodes
```

Create a secret that

```sh
kubectl create secret tls tls-secret --cert=cert.pem --key=tls.pem -oyaml --dry-run >
```

```yaml
apiVersion: v1
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS...
  tls.key: LS0tLS1CRUdJTiBQUklWQVRFIE...
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
```


```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx # newer Nginx-Ingress versions NEED THIS
  tls:
  - hosts:
      - mydomain.com
    secretName: tls-secret
  rules:
  - host: mydomain.com
    http:
      paths:
      - path: /service1
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
      - path: /service2
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 80
```

There is a way you can test this by using `curl`'s ability to resolve a domain

```sh
curl -kv https://mydomain.com:31033/service1 --resolve mydomain.com:31033:localhost
```
