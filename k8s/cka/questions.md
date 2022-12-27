# CKA Questions

This page has a list of random questions that I have found online and have tried to solve.

https://k21academy.com/docker-kubernetes/cka-ckad-exam-questions-answers/

Create a new service account with the name pvviewer. Grant this Service account access to list all PersistentVolumes in the cluster by creating an appropriate cluster role called pvviewer-role and ClusterRoleBinding called pvviewer-role-binding. Next, create a pod called pvviewer with the image: redis and serviceaccount: pvviewer in the default namespace.

```sh
# Create service account
$ kubectl create serviceaccount pvviewer

# Create cluster role
$ kubectl create clusterrole pvviewer-role --verb=list --resource=PersistentVolumes


# Create cluster role binding
$ kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer


# Verify
$ kubectl auth can-i list PersistentVolumes –as system:serviceaccount:default:pvviewer
```

- Create a new deployment called nginx-deploy, with image nginx:1.16 and 1 replica. Record the version. Next upgrade the deployment to version 1.17 using rolling update. Make sure that the version upgrade is recorded in the resource annotation.

- Create snapshot of the etcd running at https://127.0.0.1:2379. Save snapshot into /opt/etcd-snapshot.db.

- Create a Persistent Volume with the given specification. Volume Name: pv-analytics, Storage: 100Mi, Access modes: ReadWriteMany, Host Path: /pv/data-analytics

- Taint the worker node to be Unschedulable. Once done, create a pod called dev-redis, image redis:alpine to ensure workloads are not scheduled to this worker node. Finally, create a new pod called prod-redis and image redis:alpine with toleration to be scheduled on node01.

key:env_type, value:production, operator: Equal and effect:NoSchedule

```sh
$ kubectl get nodes
$ kubectl taint node node01 env_type=production:NoSchedule
$ kubectl describe nodes node01 | grep -i taint
$ kubectl run dev-redis --image=redis:alpine --dyn-run=client -o yaml > pod-redis.yaml
$ cat prod-redis.yaml
apiVersion: v1 
kind: Pod 
metadata:
  name: prod-redis 
spec:
  containers:
  - name:  prod-redis 
    image:  redis:alpine
  tolerations:
  - effect: Noschedule 
    key: env_type 
    operator: Equal 
    value: prodcution
$ kubectl create -f prod-redis.yaml
```


- Set the node named worker node as unavailable and reschedule all the pods running on it. (Drain node)

```sh
$ kubectl drain worker node --ignore-daemonsets
```

- Create a Pod called non-root-pod , image: redis:alpine, runAsUser: 1000, fsGroup: 2000

- Create a NetworkPolicy which denies all ingress traffic


```sh
$ vim policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
$ kubectl create -f policy.yaml
```
