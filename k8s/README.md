# Kubernetes

This section is a jumping off point to deeper dives on Kubernetes subjects.

Certifications
- [CKA](./cka) - Certified Kubernetes Administrator Exam

Tools:
- [Tools](tools.md) - Lens, k9s, kubectx

Kubernetes Resources:
- [ConfigMaps](configmaps.md)
- [Secrets](secrets.md)
- [ServiceAccounts and Users](users.md)

# Kubernetes Cheatsheet

Most of the info on the remainder of this page comes from the Kubernetes Cheatsheet: 

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

# Cluster Info

Display addresses and services
```sh
kubectl cluster-info
```

Dump cluster state

```sh
kubectl cluster-info dump
```

# Kube Contexts

File that contains kube configs

```sh
$HOME/.kube/config
```

List the kube context

```sh
kubectl config current-context
kubectx
```

Change the kube context

```sh
kubectx contextname
```

Specify a kube config

```sh
kubectl --kubeconfig devops.kubeconfig get all
```

# Nodes

Get info about the nodes
```sh
# Simple
kubectl get nodes

# Detailed
kubectl get nodes -o wide
```

# Namespaces

List the namespaces

```sh
kubectl get ns

kubens
```

Change the namespace

```sh
kubens namespace
```

Create/delete a namespace

```sh
kubectl create namespace new-namespace
kubectl create ns new-namespace

kubectl delete ns new-namespace
```

# kubectl

Install kubectl on Mac

```sh
brew install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
```

Install kubectl on Linux

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

Get the version

```sh
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"16", GitVersion:"v1.16.2", GitCommit:"c97fe5036ef3df2967d086711e6c0c405941e14b", GitTreeState:"clean", BuildDate:"2019-10-15T23:42:50Z", GoVersion:"go1.12.10", Compiler:"gc", Platform:"darwin/amd64"}
```

Get all items

```sh
# Get all items in the current namespace
kubectl get all

# Get all items in the namespace test
kubectl get all -n test

# Get all items in ALL namespaces
kubectl get all -A
```

Manage a kube config yaml file

```sh
kubectl apply -f pod_config.yaml
kubectl delete -f pod_config.yaml
kubectl edit -f pod_config.yaml
```

Apply all the kube configs in a folder path

```sh
kubectl apply -k folder
```

Get the bitnami Docker image

```sh
docker pull bitnami/kubectl
docker pull bitnami/kubectl:1.17
docker pull bitnami/kubectl:1.18
```

Setup a reverse proxy to securely reach ports on the cluster

```sh
kubectl proxy

curl http://localhost:8080/api/
```

Port-forward on the local host directly to a pod (5000 -> 80)

```sh
kubectl port-forward nginx --namespace app 5000:80
```

Port-forward on the local host directly to a pod (5000 -> 80) and allow all interfaces. Use this to access from outside the current machine. Useful for when the kubectl client is on the jump host OR when the cluster is on VMs on the host.

```sh
sudo ufw allow 5000
kubectl port-forward nginx --address 0.0.0.0 5000:80
```

Port-forward on the local host to a service (8001 -> 8080)

```sh
kubectl port-forward svc/nginx 8001:8080
```

# Pods

List pods

```sh
# Get all pods in current namespace
kubectl get pods
kubectl get po

# Get all pods in the namespace 'test'
kubectl get po -n test

# Get all pods in ALL namespaces
kubectl get po -A
```

Describe info about a pod 

```sh
# Text
kubectl describe po pod-name

# Yaml
kubectl describe po pod-name -o yaml
```

Delete a pod

```sh
kubectl delete po pod-name
```

Get the logs of a pod

```sh
# Get the logs of a pod
kubectl logs pod-name

# Get the logs of a pod with more than one container
kubectl logs pod-name
```

# Service

Get/Describe a service

```sh
kubectl get svc service-name
kubectl get svc service-name -n test

kubectl describe svc service-name --namespace=jenkins
```

Port forward local host to service (8000 -> 443)

```sh
kubectl port-forward -n istio-system svc/istio-ingressgateway 8000:443
```

Delete a service

```sh
kubectl delete svc service-name
```

# Secrets

Create a generic secret

```sh
# Singles
kubectl create secret generic my-secret --from-literal=key-id="key"

# Multiples
kubectl create secret generic my-secret --from-literal=key-id="key" --from-literal=access-key="key"
```

# API Resources

To get a list of all the resources and their preferred versions and shortcut name:

```sh
$ kubectl api-resources -o wide
NAME                              SHORTNAMES   APIVERSION                             NAMESPACED   KIND                             VERBS
...
pods                              po           v1                                     true         Pod                              [create delete deletecollection get list patch update watch]

```

To get a list off all versions including preferred for an api group in the `preferredVersion` field:

```sh
kubectl proxy 8002 &
curl localhost:8002/apis/rbac.authorization.k8s.io
```


To convert an old Deployment to `apps/v1`, you install the kubectl-convert plugin

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl-convert"
sudo install -o root -g root -m 0755 kubectl-convert /usr/local/bin/kubectl-convert
```


And then can run:

```sh
kubectl convert -f ./deployment-old.yaml --output-version apps/v1 > deployment-new.yaml
```

# Custom Resource Definitions (CRDs)

Custom resources require a custom controller to process. A CRD is used to define the custom resource for the controller.

Get/Describe CRDs

```sh
kubectl get crd
kubectl get crd networking.istio.io
kubectl get crd networking.istio.io -o yaml
kubectl describe crd networking.istio.io
```

Properties:
- Scoped as Namespaced or Cluster wide
- Singluar and Plural name
- Shortcut name
- Name must use plural as prefix
- Must set `storage` and `served` to true

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: foos.samplecontroller.k8s.io
spec:
  group: samplecontroller.k8s.io
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        # schema used for validation
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                deploymentName:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 10
            status:
              type: object
              properties:
                availableReplicas:
                  type: integer
  names:
    kind: Foo
    plural: foos
  scope: Namespaced
```

# Custom Resources

Custom resource of a CRD.

```yaml
apiVersion: samplecontroller.k8s.io/v1alpha1
kind: Foo
metadata:
  name: example-foo
spec:
  deploymentName: example-foo
  replicas: 1
```

# Custom Controller

A custom controller is needed to read items from ETCD and act upon them using the Kubernetes API. There is a python controller library, but people often use Go since it handles things like Queues and [Informers](https://macias.info/entry/202109081800_k8s_informers.md).

https://github.com/kubernetes/sample-controller

Controllers generally use a kubeconfig as a command-line parameter for accessing cluster resources.

# Custom Columns

Use custom columns to print out reports in interesting ways.

Print all of the containers with their pods:

```sh
kubectl get pods -A -o="custom-columns=NAMESPACE:metadata.namespace,POD:metadata.name,IMAGE:spec.containers[*].image"
NAMESPACE              POD                                         IMAGE
default                busybox-28qvh                               busybox
default                nginx                                       nginx
kube-flannel           kube-flannel-ds-26tgh                       docker.io/rancher/mirrored-flannelcni-flannel:v0.20.2
kube-flannel           kube-flannel-ds-cp276                       docker.io/rancher/mirrored-flannelcni-flannel:v0.20.2
kube-system            coredns-57575c5f89-bq969                    registry.k8s.io/coredns/coredns:v1.8.6
kube-system            coredns-57575c5f89-pl2dp                    registry.k8s.io/coredns/coredns:v1.8.6
kube-system            etcd-k8s                                    registry.k8s.io/etcd:3.5.6-0
kube-system            kube-apiserver-k8s                          registry.k8s.io/kube-apiserver:v1.24.9
kube-system            kube-controller-manager-k8s                 registry.k8s.io/kube-controller-manager:v1.24.9
kube-system            kube-proxy-fx82t                            registry.k8s.io/kube-proxy:v1.24.9
kube-system            kube-proxy-kbxk7                            registry.k8s.io/kube-proxy:v1.24.9
kube-system            kube-scheduler-k8s                          registry.k8s.io/kube-scheduler:v1.24.9
kube-system            metrics-server-5ccdd99954-skfqj             k8s.gcr.io/metrics-server/metrics-server:v0.6.2
kubernetes-dashboard   dashboard-metrics-scraper-8c47d4b5d-kr2lm   kubernetesui/metrics-scraper:v1.0.8
kubernetes-dashboard   kubernetes-dashboard-67bd8fc546-d6fqq       kubernetesui/dashboard:v2.7.0
q1                     nginx                                       nginx:1.22.1
```

Add a format file (containers.fmt)

```
NAMESPACE            POD               IMAGE
metadata.namespace   metadata.name     spec.containers[*].image
```

And it saves a bunch of typing to specify it by file name:

```sh
kubectl get pods -A -o="custom-columns-file=containers.fmt"
```



# Argo CD

Install Argo CD

```sh
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v1.7.7/manifests/install.yaml
```

Uninstall Argo CD

```sh
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v1.7.7/manifests/install.yaml
kubectl delete ns argocd
```

Access ArgoCD on port 8080

```sh
kubectl port-forward svc/argocd-server -n argocd 8080:443
``` 


Patch Argo CD to Load Balancer or back to ClusterIP:

```sh
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "ClusterIP"}}'
```

Label a namespace for istio

```sh
kubectl label namespace argocd istio-injection=enabled
```

# Minikube

Install minikube

```sh
brew install minikube
```

Version and help

```sh
minikube version
minikube
```

Main Operations

```sh
# Start a new minikube
minikube start
minikube start --memory 4096
minikube stop

# Delete the minikube
minikube delete

# Get the IP
minikube ip

# Gets/sets the current minikube profile
minikube profile
```

# nginx

Deploy nginx to cluster

```sh
# Create a 3 replica nginx deployment
kubectl create deployment nginx --image=nginx --replicas=3

# Create a service for the nginx (8080 -> 80)
kubectl create service nodeport nginx --tcp=8080:80

# Local port forward (8001 -> 80)
kubectl port-forward svc/nginx 8001:8080

# Delete the service
kubectl delete service nginx

# Delete the deployment
kubectl delete deployment nginx 
```

# Backup/Restore up ETCD

## Backup

Backups come from the API server, so you need the creds

```sh
export ETCDCTL_API=3
etcdclt snapshot save --endpoints 127.0.0.1:2379 \
 --cacert=/etc/kubernetes/pki/etcd/ca.crt
 --cert=/etc/kubernetes/pki/etcd/server.crt
 --key=/etc/kubernetes/pki/etcd/server.key
 /home/user/etcd_backup.db
```

## Restore

Restore the backup to a new etcd data dir

```sh
mkdir /var/lib/etcd-restore-location

export ETCDCTL_API=3
etcdclt snapshot restore --data-dir /var/lib/etcd-restore-location /home/user/etcd_backup.db
```

And then edit the static manifest for etcd:

```
vi /etc/kubernetes/manifest/etcd.yaml
```

And change the `hostPath:` from `/var/lib/etcd` to `/var/lib/etcd-restore-location`.

# Tekton

Install pipeline and dashboard

```sh
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
kubectl apply -f https://storage.googleapis.com/tekton-releases/dashboard/latest/tekton-dashboard-release.yaml
```

Expose the Tekton dashboard

```sh
kubectl --namespace tekton-pipelines port-forward svc/tekton-dashboard 9097:9097
```