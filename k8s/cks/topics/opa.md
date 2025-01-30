# Open Policy Agent

Open Policy Agent (OPA) is an Admission Controller. You can use it to enforce policies of whether pods can be created for example.

OPA:
- General purpose engine
- Not Kubernetes specific
- Easy language implementation (Rego)
- Works with both JSON and YAML

OPA Gatekeeper
- Provides CRDs that make it easier to use OPA

# CRDs

The Custom Resource Definitions (CRD) implement:
- Constraint Template (eg. Required Labels)
- Constraint that is an implementation of that template

Constraint Templates create CRDs that are used by constraints

# Install OPA Gatekeeper

Check to make sure there are no other Admission Controllers installed in API Server:

```sh
$ grep "admission" /etc/kubernetes/manifests/kube-apiserver.yaml
    - --enable-admission-plugins=NodeRestriction
```

Only using `NodeRestriction`. That's good.

Now install the gatekeeper:

```sh
kubectl apply -f https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/course-content/opa/gatekeeper.yaml
```

After install you should have a gatekeeper-system namespace:

```sh
$ kubectl get ns
NAME                   STATUS   AGE
default                Active   7d1h
gatekeeper-system      Active   27s
kube-node-lease        Active   7d1h
kube-public            Active   7d1h
kube-system            Active   7d1h
kubernetes-dashboard   Active   6d23h
```

You should see the controller manager and webhook service:

```sh
$ kubectl get all -n gatekeeper-system
NAME                                                 READY   STATUS    RESTARTS   AGE
pod/gatekeeper-audit-6859697479-qp8dj                1/1     Running   0          93s
pod/gatekeeper-controller-manager-5f9f699cb8-hjpvk   1/1     Running   0          93s
pod/gatekeeper-controller-manager-5f9f699cb8-hxtxs   1/1     Running   0          93s
pod/gatekeeper-controller-manager-5f9f699cb8-z5l8g   1/1     Running   0          93s

NAME                                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/gatekeeper-webhook-service   ClusterIP   10.246.0.109   <none>        443/TCP   93s

NAME                                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/gatekeeper-audit                1/1     1            1           93s
deployment.apps/gatekeeper-controller-manager   3/3     3            3           93s

NAME                                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/gatekeeper-audit-6859697479                1         1         1       93s
replicaset.apps/gatekeeper-controller-manager-5f9f699cb8   3         3         3       93s
```

As part of the installation, there should have also been the Validating webhook. Every pod creation should pass through it:

```sh
validatingwebhookconfiguration.admissionregistration.k8s.io/gatekeeper-validating-webhook-configuration
```

The Gatekeeper is not a mutating webhook which allows you to change a pod definition.

# Creating a Deny All Policy

In GitHub there is a template:

https://github.com/killer-sh/cks-course-environment/blob/master/course-content/opa/deny-all/alwaysdeny_template.yaml

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8salwaysdeny
spec:
  crd:
    spec:
      names:
        kind: K8sAlwaysDeny
      validation:
        # Schema for the `parameters` field
        openAPIV3Schema:
          properties:
            message:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8salwaysdeny

        violation[{"msg": msg}] {
          1 > 0
          msg := input.parameters.message
        }
```

And then the implementation of that template:

https://github.com/killer-sh/cks-course-environment/blob/master/course-content/opa/deny-all/all_pod_always_deny.yaml

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAlwaysDeny
metadata:
  name: pod-always-deny
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    message: "ACCESS DENIED!"
```

- `K8sAlwaysDeny` is the connector between the template and the constraint implmentations
- The `rego` section there is a condition if it passes or fails then it prints out the message
- In this case it prints "Access Denied!" if you create **any** kind of Pod
- The OPA will only deny **new** pods that are started, it won't stop existing
- If you describe the constraint it will show how many violations there are in total including running pods.
- All booleans in the violation must be true. If one of them is false then it succeeds.

## Create a policy that requires labels on a namespace

Create a constraint template that enforces that a namespace has a certain label

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        # Schema for the `parameters` field
        openAPIV3Schema:
          properties:
            labels:
              type: array
              items: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("you must provide labels: %v", [missing])
        }
```

And then a constraint that forces namespaces to have a `k8s` label

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: ns-must-have-k8s
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["k8s"]
```

## The REGO Playground

Web App for playing with REGO code that is used for policies

https://play.openpolicyagent.org/
