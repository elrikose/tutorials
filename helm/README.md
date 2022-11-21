# Helm

When deploying applications to Kubernetes using yaml manifests you often need definitions for:

- Deployments
- Secrets
- PVs
- PVCs

If you have to change one of the manifests you often have to touch all of the manifests. You could put all of the items in one manifest, but then you have to manage the single file which get unweildy.

## What is Helm?

It changes the paradigm. It is often called a "package manger" or "installer" for Kubernetes. It assembles all of the items together that would be tedious to manage on their own. There is a single command to install:

```sh
helm install postgres ...
```

And there is a `values.yaml` file that can be used to overrid settings that you want to change. You can upgrade/rollback and only the objects that changed will be upgraded or rolled back. 

```sh
helm upgrade postgres ...
```
```sh
helm rollback postgres ...
```

And finally a simple uninstall.

```sh
helm uninstall postgres ...
```

## Installing Helm

https://helm.sh/docs/intro/install/

For Mac:

```
brew install helm
```

## values.yaml

If you want to override a value in a manifest file you specify the manifests in a template:

```yaml
   image: {{ .Values.image }}
```

And then in the values.yaml, specify the values:

```yaml
image: postgres:15.1
...
```

# Helm Chart

The combination of the templates, the `values.yaml` file, and the `Chart.yaml` is considered a "Helm Chart". The Chart.yaml contais the metadata about the chart:

https://github.com/bitnami/charts/blob/main/bitnami/postgresql/Chart.yaml

```yaml
annotations:
  category: Database
apiVersion: v2
appVersion: 15.1.0
dependencies:
  - name: common
    repository: https://charts.bitnami.com/bitnami
    tags:
      - bitnami-common
    version: 2.x.x
description: PostgreSQL (Postgres) is an open source object-relational database known for reliability and data integrity. ACID-compliant, it supports foreign keys, joins, views, triggers and stored procedures.
engine: gotpl
home: https://github.com/bitnami/charts/tree/main/bitnami/postgresql
icon: https://bitnami.com/assets/stacks/postgresql/img/postgresql-stack-220x234.png
keywords:
  - postgresql
  - postgres
  - database
  - sql
  - replication
  - cluster
maintainers:
  - name: Bitnami
    url: https://github.com/bitnami/charts
name: postgresql
sources:
  - https://github.com/bitnami/containers/tree/main/bitnami/postgresql
  - https://www.postgresql.org/
version: 12.1.2
```

Charts can be found at [ArtifactHub.io](https://artifacthub.io). You search for charts from the command-line with

```sh
$ helm search hub postgres
URL                                               	CHART VERSION	APP VERSION	DESCRIPTION
https://artifacthub.io/packages/helm/nicholaswi...	0.1.0        	13.3       	The World's Most Advanced Open Source Relationa...
https://artifacthub.io/packages/helm/krakazyabr...	0.1.0        	13.3       	The World's Most Advanced Open Source Relationa...
https://artifacthub.io/packages/helm/smo-helm-c...	6.0.0        	           	ONAP Postgres Server
https://artifacthub.io/packages/helm/lsst-sqre/...	0.1.1        	1.0        	Postgres RDBMS for LSP
https://artifacthub.io/packages/helm/groundhog2...	0.4.1        	15.1       	A Helm chart for PostgreSQL on Kubernetes
...
```

To add another repo for searching:

```sh
$ helm repo add bitnami https://charts.bitnami.com/bitnami
```

And you can list existing repos by the `list` command:

```sh
$ helm repo list
NAME   	URL
jenkins	https://charts.jenkins.io
bitnami	https://charts.bitnami.com/bitnami
```

And you can search 

## Releases

Releases are names used specify a helm chart deployment and are unique.

### Install Releases

To install you must use a release name:

```sh
helm install postgres-release bitnami/postgresql
```

You can install multiple releases with the same chart:

```sh
helm install postgres-release-1 bitnami/postgresql
helm install postgres-release-2 bitnami/postgresql
helm install postgres-release-3 bitnami/postgresql
```

### Listing Releases

To list the releases

```
helm list
```

### Listing Releases

To unistall a release

```
helm uninstall postgres-release-3
```

## Other Helm Commands

Pull a chart as a tarball:

```sh
helm pull bitnami/postgresql
```

Pull a chart and expand

```sh
helm pull --untar bitnami/postgresql
```

