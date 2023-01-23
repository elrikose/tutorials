# CKA Mock Exam 3

1. Create a new service account with the name `pvviewer`. Grant this Service account access to list all `PersistentVolumes` in the cluster by creating an appropriate cluster role called `pvviewer-role` and `ClusterRoleBinding` called `pvviewer-role-binding`.
Next, create a pod called `pvviewer` with the image: `redis` and serviceAccount: `pvviewer` in the `default` namespace.
- ServiceAccount: `pvviewer`
- ClusterRole: `pvviewer-role`
- ClusterRoleBinding: `pvviewer-role-binding`
- Pod: `pvviewer`
- Pod configured to use ServiceAccount `pvviewer` ?

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: null
  name: pvviewer
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  creationTimestamp: null
  name: pvviewer-role
rules:
- apiGroups:
  - ""
  resources:
  - persistentvolumes
  verbs:
  - list
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  creationTimestamp: null
  name: pvviewer-role-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: pvviewer-role
subjects:
- kind: ServiceAccount
  name: pvviewer
  namespace: default
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pvviewer
  name: pvviewer
spec:
  containers:
  - image: redis
    name: pvviewer
    resources: {}
  serviceAccount: pvviewer
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```


2. List the `InternalIP` of all nodes of the cluster. Save the result to a file `/root/CKA/node_ips`.
Answer should be in the format: 

```
InternalIP of controlplane<space>InternalIP of node01 (in a single line)
```

```sh
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'
```

3. Create a pod called `multi-pod` with two containers. 
Container 1, name: `alpha`, image: `nginx`
Container 2: name: `beta`, image: `busybox`, command: `sleep 4800` 

Environment Variables:
- container 1: `name: alpha`
- container 2: `name: beta`

Requirements
- Pod Name: multi-pod
- Container 1: alpha
- Container 2: beta
- Container beta commands set correctly?
- Container 1 Environment Value Set
- Container 2 Environment Value Set

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: multi-pod
  name: multi-pod
spec:
  containers:
  - image: nginx
    name: alpha 
    env:
    - name: name
      value: alpha
  - args:
    - sleep
    - "4800"
    image: busybox
    name: beta
    env:
    - name: name
      value: beta
```

4. Create a Pod called `non-root-pod` , image: `redis:alpine`
```yaml
runAsUser: 1000
fsGroup: 2000
```
- Pod `non-root-pod` fsGroup configured
- Pod `non-root-pod` runAsUser configured

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: non-root-pod
spec:
  containers:
  - image: redis:alpine
    name: non-root-pod
  securityContext:
    runAsUser: 1000
    fsGroup: 2000
```

5. We have deployed a new pod called `np-test-1` and a service called `np-test-service`. Incoming connections to this service are not working. Troubleshoot and fix it.
Create `NetworkPolicy`, by the name `ingress-to-nptest` that allows incoming connections to the service over port `80`.
Important: Don't delete any current objects deployed.
Important: Don't Alter Existing Objects!
- NetworkPolicy: Applied to All sources (Incoming traffic from all pods)?
- NetWorkPolicy: Correct Port?
- NetWorkPolicy: Applied to correct Pod?

This is currently denied:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

Create an allow:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-nptest
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - protocol: TCP
          port: 80
```

Solution manifest file to create a network policy ingress-to-nptest as follows:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-nptest
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: np-test-1
  policyTypes:
  - Ingress
  ingress:
  - ports:
    - protocol: TCP
      port: 80
```

6. Taint the worker node `node01` to be `Unschedulable`. Once done, create a pod called `dev-redis`, image `redis:alpine`, to ensure workloads are not scheduled to this worker node. Finally, create a new pod called `prod-redis` and image: `redis:alpine` with toleration to be scheduled on node01.
key: `env_type`, value: `production`, operator: `Equal` and effect: `NoSchedule`
- Key = `env_type`
- Value = `production`
- Effect = `NoSchedule`
- pod 'dev-redis' (no tolerations) is not scheduled on node01?
Create a pod 'prod-redis' to run on node01



7. Create a pod called `hr-pod` in `hr` namespace belonging to the `production` environment and `frontend` tier .
image: `redis:alpine`
Use appropriate labels and create all the required objects if it does not exist in the system already.
- `hr-pod` labeled with environment production?
- `hr-pod` labeled with tier frontend?

```sh
# Create a namespace if it doesn't exist:
kubectl create namespace hr

# and then create a hr-pod with given details:
kubectl run hr-pod --image=redis:alpine --namespace=hr --labels=environment=production,tier=frontend
```

8. A `.kubeconfig` file called `super.kubeconfig` has been created under `/root/CKA`. There is something wrong with the configuration. Troubleshoot and fix it.

Wrong port. It was 9999 instead of 6443

9. We have created a new deployment called `nginx-deploy`. scale the deployment to 3 replicas. Has the replica's increased? Troubleshoot the issue and fix it.
deployment has 3 replicas

Use the command kubectl scale to increase the replica count to 3.

```sh
kubectl scale deploy nginx-deploy --replicas=3
```

The controller-manager is responsible for scaling up pods of a replicaset. If you inspect the control plane components in the kube-system namespace, you will see that the controller-manager is not running.

```sh
kubectl get pods -n kube-system
```

The command running inside the controller-manager pod is incorrect. 
After fix all the values in the file and wait for controller-manager pod to restart. 

Alternatively, you can run sed command to change all values at once:
`sed -i 's/kube-contro1ler-manager/kube-controller-manager/g' /etc/kubernetes/manifests/kube-controller-manager.yaml`
This will fix the issues in controller-manager yaml file.
At last, inspect the deployment by using below command:
kubectl get deploy
