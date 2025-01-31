# Kubernetes Auditing

API requests are made. You can tell Kubernetes to save all of the API requests made.

Why?
- Did someone access a secret while it wasn't protected
- When was the last time that user X accessed cluster Y
- Does my CRD work properly?

There are 4 Stages to an API Request:
- RequestReceived - Events that happen as soon as the handler receives the request
- ResponseStarted - After Response Headers are sent, but before Response Body. Only generated for long requests
- ResponseComplete - No more bytes will be sent as the body is finished
- Panic - when something bad happens

You can set which Audit Policy Stages you even want to log.

Which events should you record? Depends on how many requests are being made. It could be a firehose.

There are 4 Audit Policy Levels
- None - don't log events that match the rule
- Metadata - log metadata but not request/request body
- Request - log event metadata and request body, but not response body
- RequestResponse - log event metadata and request body and response body

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived" # no data from RequestReceived
rules:

# log no "read" actions
- level: None
  verbs: ["get", "watch", "list"]

# log nothing regarding events
- level: None
  resources:
  - group: "" # core
    resources: ["events"]

# log nothing coming from some groups
- level: None
  userGroups: ["system:nodes"]

- level: RequestResponse
  resources:
  - group: ""
    resources: ["secrets"]

# for everything else log metadata
- level: Metadata
```

Events are handled in order

Where to store all of the data?
- Stored in json file
- Webhook logs
- Dynamice backend

Injested by other services like Datadog or Elasticsearch

# Configuration

Configuration requires the `policy.yaml` file setup for the API server

1. Change the policy file
2. Disable auditing in API server, then restart
3. Re-enable auditing in API server, then restart
4. Test your changes

If it doesn't restart check the logs via:

- `cat /var/log/containers/kube-apiserver`
- `crictl ps kube-apiserver-master`

To enable audit logging, add to the kube-apiserver static manifest:

```yaml
    - kube-apiserver
    - --audit-policy-file=/etc/kubernetes/audit/policy.yaml
    - --audit-log-path=/etc/kubernetes/audit/logs/audit.log
    - --audit-log-maxsize=500
    - --audit-log-maxbackup=5
```

You also have to add the volume paths:

```yaml
    volumeMounts:
...
    - mountPath: /etc/kubernetes/audit
      name: k8s-audit
      readOnly: false
...
  volumes:
...
  - hostPath:
      path: /etc/kubernetes/audit
      type: DirectoryOrCreate
    name: k8s-audit
```

Now in the audit logs, json should be created in `/etc/kubernetes/audit/logs/audit.log` with all items logged at the `Metadata` level:

```json
...
{"kind":"Event","apiVersion":"audit.k8s.io/v1","level":"Metadata","auditID":"405318cf-ba4b-46d0-a9b3-53a6e17d9669","stage":"RequestReceived","requestURI":"/apis/crd.projectcalico.org/v1/ipamblocks?allowWatchBookmarks=true\u0026resourceVersion=1661164\u0026timeout=7m18s\u0026timeoutSeconds=438\u0026watch=true","verb":"watch","user":{"username":"system:kube-controller-manager","groups":["system:authenticated"]},"sourceIPs":["10.154.161.198"],"userAgent":"kube-controller-manager/v1.29.6 (linux/amd64) kubernetes/062798d/metadata-informers","objectRef":{"resource":"ipamblocks","apiGroup":"crd.projectcalico.org","apiVersion":"v1"},"requestReceivedTimestamp":"2024-06-30T19:41:14.278898Z","stageTimestamp":"2024-06-30T19:41:14.278898Z"}
{"kind":"Event","apiVersion":"audit.k8s.io/v1","level":"Metadata","auditID":"405318cf-ba4b-46d0-a9b3-53a6e17d9669","stage":"ResponseStarted","requestURI":"/apis/crd.projectcalico.org/v1/ipamblocks?allowWatchBookmarks=true\u0026resourceVersion=1661164\u0026timeout=7m18s\u0026timeoutSeconds=438\u0026watch=true","verb":"watch","user":{"username":"system:kube-controller-manager","groups":["system:authenticated"]},"sourceIPs":["10.154.161.198"],"userAgent":"kube-controller-manager/v1.29.6 (linux/amd64) kubernetes/062798d/metadata-informers","objectRef":{"resource":"ipamblocks","apiGroup":"crd.projectcalico.org","apiVersion":"v1"},"responseStatus":{"metadata":{},"code":200},"requestReceivedTimestamp":"2024-06-30T19:41:14.278898Z","stageTimestamp":"2024-06-30T19:41:14.280316Z","annotations":{"authorization.k8s.io/decision":"allow","authorization.k8s.io/reason":"RBAC: allowed by ClusterRoleBinding \"system:kube-controller-manager\" of ClusterRole \"system:kube-controller-manager\" to User \"system:kube-controller-manager\""}}
```

# Exercise: Create a secret and find it in the logs

Create a secret:

```sh
k create secret generic very-secure --from-literal=pass=supersecret
```

Now find it in the logs:

```sh
grep very-secure * | jq .
{
  "kind": "Event",
  "apiVersion": "audit.k8s.io/v1",
  "level": "Metadata",
  "auditID": "1159a180-206c-47be-ae82-9fec4320ec62",
  "stage": "ResponseComplete",
  "requestURI": "/api/v1/namespaces/default/secrets?fieldManager=kubectl-create&fieldValidation=Strict",
  "verb": "create",
  "user": {
    "username": "kubernetes-admin",
    "groups": [
      "kubeadm:cluster-admins",
      "system:authenticated"
    ]
  },
  "sourceIPs": [
    "10.154.161.1"
  ],
  "userAgent": "kubectl/v1.30.2 (linux/amd64) kubernetes/3968350",
  "objectRef": {
    "resource": "secrets",
    "namespace": "default",
    "name": "very-secure",
    "apiVersion": "v1"
  },
  "responseStatus": {
    "metadata": {},
    "code": 201
  },
  "requestReceivedTimestamp": "2024-06-30T19:50:00.702188Z",
  "stageTimestamp": "2024-06-30T19:50:00.708378Z",
  "annotations": {
    "authorization.k8s.io/decision": "allow",
    "authorization.k8s.io/reason": "RBAC: allowed by ClusterRoleBinding \"kubeadm:cluster-admins\" of ClusterRole \"cluster-admin\" to Group \"kubeadm:cluster-admins\""
  }
}
```

# Exercise: Restrict Logged data

- Nothing from RequestReceived
- Nothing from "get", "watch", "list"
- From Secrets only metadata level
- Everything else RequestResponse level

```yaml
apiVersion: audit.k8s.io/v1 # This is required.
kind: Policy
# Nothing from RequestReceived.
omitStages:
  - "RequestReceived"
rules:
  # Nothing from "get", "watch", "list"
  - level: None
    verbs: ["get", "watch", "list"]

  # From Secrets only metadata level
  - level: Metadata
    resources:
    - group: ""
      resources: ["secrets"]

  # Everything else RequestResponse level
  - level: RequestResponse
    omitStages:
      - "RequestReceived"
```
