# Argo CD

Many of the notes come right from this [Udemy course](https://www.udemy.com/course/argo-cd-essential-guide-for-end-users-with-practice/) along with my own research using other materials.

The best description for Argo CD is right from the documentation:

https://argo-cd.readthedocs.io/en/stable/

>Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.

Argo CD is better than Jenkins or other CI tools:
- It is Kubernetes Native
- Highly opinionated on GitOps. Git changes cause deployment changes to the application
- ArgoCD manages Git and Cluster status and keeps them in sync

Argo CD supports
- Kubernetes Yaml Manifests
- Helm Charts
- Kustomize

You still need a CI system to build your images and deploy to an image repository.

# Deployment

```sh
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Open a port forward:

```sh
kubectl port-forward -n argocd svc/argocd-server 8080:443
```

Get the initial admin password:

```sh
kubectl get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
```

On Linux open the port

```sh
sudo ufw allow 8080/tcp
```

# Installing the Argo CD CLI

Argo CD comes with a CLI tool that makes it easier from your CI system to manage

- Applications
- Repos
- Clusters
- Admin Tasks
- Projects

Installation on Linux:

```sh
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

And then login, using the `admin` and password from above:

```sh
argocd login localhost:8080
```

# Creating Applications

There are three ways to creating applications in Argo CD:

- Yaml Manifests (preferred for GitOps)
- Web UI
- `argocd` CLI

When you install Argo CD, you install CRDs in the cluster, including one for `Application`. Applications require the definition of:

- Application Name
- Project Name
- Source repository
- Destination cluster

Here is an example Yaml Manifest that has all of these values:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-app
  namespace: argocd
spec:
  project: web-apps
  source:
    repoURL: "https://github.com/emartin-hv/argocd-apps"
    path: web-apps/nginx-app
    targetRevision: main
  destination: 
    namespace: web
    server: "https://kubernetes.default.svc"
```

In the example: 

- Application Name: nginx-app
- Project Name: web-apps
- Source repository: https://github.com/emartin-hv/argo-apps (master branch)
- Destination cluster: https://kubernetes.default.svc (local cluster -- web namespace)

In the CLI you'd write something like this:

```sh
argocd app create web-apps --repo https://github.com/emartin-hv/argo-apps --path nginx-app --dest-server https://kubernetes.default.svc --dest-namespace web
```

How does Argo CD know what is in the source repo path?

- If there is a `Chart.yaml`, assumes that it is a helm chart
- If there are `kustomization.yaml`, `kustomization.yml`, or `Kustomization`, assumes kustomize
- Else it assumes Kubernetes manifests

# Helm Deployments

Helm deployments can be used to specify values files and parameters in the yaml:

```yaml
source:
  chart: nginx
  repoURL: https://charts.bitnami.com/bitnami
  targetRevision: 1.23.4 # chart version
  helm:
    releaseName: nginx-app # defaults to chart name
    valuesFiles:
    - values.yaml
    parameters:
    - name: foo
      value: bar
```

Values can also be overrode by an inline values

```yaml
source:
  helm:
    values: |
      foo: bar
      bar: baz
```

# Kustomize Deployments

When deploying with Kustomize you can choose:

- Name prefix
- Name suffix
- Image
- Labels
- Annotations
- Force a kustomize version

Cluster resources that are created will have a prefix or suffix

```yaml
source:
  path: foo
  repoURL: "https://..."
  kustomize:
    namePrefix: "myapp-"
    nameSuffix: "-staging"
    images:
    - nginx:latest
    commonLabels:
      app: myapp
      env: staging
    commonAnnotations:
      environment: staging
    version: v3.5.1
```

# Projects

Argo CD Projects are a way to group applications logically. You can configure the following:

- Name
- Description
- Source repos
- Destination clusters and namespaces
- Cluster resources whitelist
- Cluster resources blacklist


Items that have no constraint use a `*`. Here is an example that doesn't liit anything:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: web-apps
  namespace: argocd
spec:
  description: "Web Apps"
  sourceRepos:
  - '*'
  destinations:
  - namespace: '*'
    server: '*'
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'
```

Here is an example that limits the applications to the local cluster and 1 repo:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: web-apps
  namespace: argocd
spec:
  description: "Web Apps"
  sourceRepos:
  - 'https://github.com/emartin-hv/argocd-apps'
  destinations:
  - namespace: 'web'
    server: "https://kubernetes.default.svc"
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'
```

# Git Repositories

Argo CD supports both public and private git repositories

- Public repositories can be used without specifying creds
- Private repositories have to be registered with the application before use

Git connection methods

- HTTPS - username, password, token
- SSH - SSH private key

Repo credentials are stores in normal Kubernetes secrets. They can be registered declaratively, Web UI, or CLI. The secret must specify a label of `argocd.argoproj.io/secret-type: repository` and a data type of `git`.

# Helm Repositories

Argo CD supports both public and private helm repositories

- Public repositories can be used without specifying creds
- Private repositories have to be registered with the application before use

Repo credentials are stores in normal Kubernetes secrets. They can be registered declaratively, Web UI, or CLI. The secret must specify a label of `argocd.argoproj.io/secret-type: repository` and a data type of `helm`. You also must pass:

- Name of the repo
- Repo URL
- username/password OR
- TLS cert and key

# Credential Templates

Useful for using the same credentials for multiple repositories using the label `argocd.argoproj.io/secret-type: repo-creds`. The URL configured for the template must be a prefix of the repository URL. They can be registered declaratively, Web UI, or CLI.

Via CLI:

```sh
argocd repocreds add https://github.com/emartin-hv --user git --password secret
```

In the UI, you simply **Save as Credentials Template** when saving the secret.

# Automated Sync

ArgoCD polls every 3 minutes to see if there is a change in a repository. A sync then has to manually be invoked by the UI or CLI. You can also configure to automatically sync if a change is recognized. Caveats:

- Sync only happens if it is "Out of Sync" not other statuses like "Unknown"
- If a sync fails, it won't retry for the same git commit.
- Define automated sync declaratively using the `syncPolicy:` top level map:

```yaml
syncPolicy:
  automated: {}
```

With the CLI you specify `--sync-policy`:

```sh
argocd app create foo ... --sync-policy automated
```

In the UI, it is an application setting.

# Automated Pruning

By default, automated sync doesn't delete the cloud resources (pruning). In the `syncPolicy:` section in a declarative manifest you can set pruning to automated via `prune: true`:

```yaml
syncPolicy:
  automated:
    prune: true
```

With the CLI you specify `--auto-prune`:

```sh
argocd app create foo ... --auto-prune
```

In the UI, it is an application setting. Or when you manually sync you can choose to Prune.

# Automated Self Healing

If you manually make a change to a cluster, Argo CD has the ability to "heal" back to what the state is in the cluster. In the `syncPolicy:` section in a declarative manifest you can set pruning to automated via `prune: true`:

```yaml
syncPolicy:
  automated:
    selfHeal: true
```

With the CLI you specify `--self-heal`:

```sh
argocd app create foo ... --self-heal
```

In the UI, it is an application setting.

# Sync Options

There are other options besides pruning and creating namespaces. You can set options at the application and resource level.

## Resource Level options

You can set at the Kubernetes resource level sync options like not pruning ever

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false
```

## Selective Sync

Selective Sync is for only synching resources that are out of sync. Which is useful when you have tons of resources. Only applicable at the application level via `ApplyOutOfSyncOnly=true`.

## Prune Last

At the application or resource level you can choose that pruning will happen after creation via `PruneLast=true`.

# Sync Phases

There are 3 sync phases

- PreSync - Database migrations, etc
- Sync - App Manifests are applied
- PostSync - Send notifications

To cause an action to happen you specify the `argocd.argoproj.io/hook: PreSync` or `argocd.argoproj.io/hook: PostSync` annotation and then those will be run only during those phases. A good use case would be a Kubernetes Job (database migration)

There are also 2 resource hook types:

- Skip - when Argo CD skips a sync
- SyncFail - when a sync fails

# Sync Waves

Sync Waves are a way to set a wave number on a manifest so that resources are created in an certain order for each sync phase (PreSync, Sync, PostSync). For example secret before a backend pod which is before a front end pod. 

- Default wave if you don't specify it is 0.
- Waves are number, including negative numbers. 
- Negative numbers happen before positive
- Next wave starts after previous resources are Ready.


Declaratively specified by `argocd.argoproj.io/sync-wave` annotation.

```yaml
apiVersion: apps/v1
kind: Job
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
```

# Deploying to Kubernetes Clusters

By default, Argo CD has the ability to deploy into the local cluster. Other clusters including the authentication can be added by using secrets. 

- Each secret must have a label of `argocd.argoproj.io/secret-type: cluster`
- Secret must have name, server url, config, optional namespace
- Authentication can be by:
  - Basic
  - Bearer tokens
  - IAM configuration
  - External provider

Possible to add the secret by the `argocd` CLI:

```sh
argocd cluster add <context> # Context name in KUBECONFIG
```

# ApplicationSet

An ApplicationSet is a way to manage multiple applications potentially on multiple clusters. 

ApplicationSets have generators (parameters) that can be used to specify multiple values to a template. Declaratively in a manifest: 

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: nginx-appset
spec:
  generators:
  - list:
    elements:
    - cluster: cluster-1
      url: https://url1
    - cluster: cluster-1
      url: https://url1
template:
  metadata:
    name: "{{cluster}}-nginx"

  spec:
    destination:
      server: cluster-1
      namespace: nginx
    source:
      repoURL: "{{url}}"
      targetRevision: main
      path: "guestbook/{{cluster}}"
```

Generator types:
- List generator - key/values for substitution in the template
- Cluster generator - generate apps based on cluster names
- Git generator - generate apps based on files in a Git repository
  - Git file generator - json/yaml based file parameters
  - Git directory generator - directory structure based parameters
- Matrix generator - combine parameters from 2 separate generators
- Merge generator - merge generated parameters from 2 or more separate generators
- Pull Request generator - generate apps based on Pull Requests in a repository

The most compelling here is the Git directory generator because you can point it to a git repo that defines the apps and they can be deployed by app name. 

A matrix generator is useful to mix a Cluster generator with a Git folder generator to support multiple clusters.