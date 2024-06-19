# Ingress

What is Ingress?

There are many different types of Ingress controllers.

The most popular is a pod with nginx in it. The Kubernetes manifest wraps around nginx so that you don't have to edit Nginx configuration files.

Ingress requires a LoadBalancer. LoadBalancer requires a NodePart service that requires a ClusterIP service.