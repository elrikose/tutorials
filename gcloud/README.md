# Google Cloud

## Initialize 

Initialize the gcloud CLI

```
gcloud init
```

Authenticate with the Google Cloud SDK

```
gcloud auth application-default login
``` 

Update the CLI components

```
gcloud components update
```

Enable services:

```
gcloud services enable container.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

## Projects

List the projects:

```
$ gcloud projects list
PROJECT_ID         NAME        PROJECT_NUMBER
my-project-12345   My Project  144330123884
```

Set the default project (--project)

```
$ gcloud config set core/project my-project-12345
Updated property [core/project].
```

## Configuration

List the user configurations

```
$ gcloud config configurations list
NAME     IS_ACTIVE  ACCOUNT             PROJECT            COMPUTE_DEFAULT_ZONE  COMPUTE_DEFAULT_REGION
cloud    True       cloud@emailcom      my-project-12345   us-central1-a         us-central1
default  False      erik@gmail.com      new-project-236104
```

Activate a confiuration by name

```
gcloud config configurations activate cloud
```

List the gcloud config for this configuration

```
$ gcloud config list
[compute]
region = us-central1
zone = us-central1-a
[core]
account = cloud@emailcom
project = my-project-12345
```

Set the account

```
gcloud config set core/account cloud@email.com
``` 

Set the default project for commands

```
gcloud config set core/project my-project-12345
```

Set  default region and zone
```
gcloud config set compute/region us-east1
gcloud config set compute/zone us-east1-b
``` 

# GCE

Google Compute Engine

List the compute instances

```
gcloud compute instances list
gcloud compute instances list --project my-project-12345
```

SSH into the user VM

```
gcloud compute ssh user@gce-vm --zone us-central1-a
```

Describe a VM

```
gcloud compute instances describe gce-vm --zone us-central1-a
```

List all of the IP addresses

```
gcloud compute addresses list
gcloud compute addresses list --global
```

Delete an IP address named "loadbalancer-ip"

```
gcloud compute addresses delete loadbalancer-ip
```

# GKE

Google Kubernetes Engine

Get the Kube config for the cluster

```
gcloud container clusters get-credentials cicd-cluster --zone us-central1-c --project my-project-12345
```

Login to the node pool VM

```
gcloud compute ssh gke-node-pool-ec079e2b-l9gp --zone us-central1-c --internal-ip
```

List the health checks

```
gcloud compute health-checks list
```

# Cloud DNS

List the managed zones
```
gcloud dns managed-zones list
```

List the records for the managed zone

```
gcloud dns record-sets list --zone=dns-zone
```
 