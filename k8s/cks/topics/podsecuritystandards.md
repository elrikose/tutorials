# Pod Security Standards

There are 3 profiles:

- Privileged - entirely unrestricted
- Baseline - aimed at easing adoption for most workloads
- Restricted - enforces pod hardening

There are three levels:

- enforce - rejects Pods with policy violations.
- audit - allows pods with policy violations but includes an audit annotation in the audit log event record.
- warn - allows pods with policy violations but warns users.

# Namespace

You set Pod Security Standards at the namespace via labels:

```sh
kubectl label --overwrite ns example \
  pod-security.kubernetes.io/enforce=baseline \
  pod-security.kubernetes.io/enforce-version=v1.32 \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/warn-version=v1.32 \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/audit-version=v1.32
```

And this is how it looks like in the config

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-baseline-namespace
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/enforce-version: v1.32
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: v1.32
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: v1.32
```

# Cluster

Set the `AdmissionConfiguration` in say a `/etc/kubernetes/pss/pss.yaml`:

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
 - name: PodSecurity
   configuration:
     apiVersion: pod-security.admission.config.k8s.io/v1
     kind: PodSecurityConfiguration
     defaults:
       enforce: "baseline"
       enforce-version: "latest"
       audit: "restricted"
       audit-version: "latest"
       warn: "restricted"
       warn-version: "latest"
     exemptions:
       usernames: []
       runtimeClasses: []
       namespaces: [kube-system]
```

And than in the `kube-apiserver` you set the value:

```sh
   - --admission-control-config-file=/etc/config/cluster-level-pss.yaml
```
