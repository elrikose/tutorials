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

 5399  gcloud compute http-health-checks list
 5400  gcloud compute https-health-checks list
 5401  gcloud compute health-checks list
 5402  gcloud compute health-checks delete piplup-cluster-healthcheck
 5404  gcloud compute health-checks describe pikachu-cluster-healthcheck
 5405  gcloud compute forwarding-rules list
 5406  gcloud compute forwarding-rules describe pikachu-cluster-lb-frontend
 5408  gcloud compute backend-services list
 5409  gcloud compute backend-services describe pikachu-cluster-lb\ --region=us-central1
 5410  gcloud compute backend-services describe pikachu-cluster-lb --region=us-central1
 5412  gcloud compute forwarding-rules list
 5413  gcloud compute forwarding-rules describe pikachu-cluster-lb-frontend --region us-central1
 5414  gcloud compute firewall-rules list
 5417  gcloud compute target-pools list
 5418  gcloud compute target-pools list --format=json
 5420  gcloud compute backend-services list
 5421  gcloud compute health-checks list
 5422  gcloud compute health-checks describe piplup-cluster-healthcheck
 5423  gcloud compute forwarding-rules describe piplup-cluster-lb-frontend
 5424  gcloud compute backend-services describe piplup-cluster-lb --region=us-central1
 5438  gcloud compute addresses list
 5439  gcloud compute addresses list | grep char
 5444  gcloud compute instance-groups list
 5454  gcloud compute instance-groups describe gke-charmander-clust-charmander-node--4fdefd6c-grp
 5455  gcloud compute instance-groups describe gke-charmander-clust-charmander-node--4fdefd6c-grp --zone us-central1-c
 5862  gcloud compute addresses list
 5864  gcloud compute backend-services list
 5865  gcloud dns record-sets list
 5866  gcloud dns record-sets list --zone=hitachi-lumada-io-zone
 5896  gcloud project
 5897  gcloud config
 5898  gcloud config list
 5899  gcloud config set
 5900  gcloud config set project pentaho-lee-cheng
 5901  gcloud config list
 5909  gcloud kms
 5910  gcloud keyrings list
 5911  gcloud kms keyrings list
 5912  gcloud kms keyrings
 5913  gcloud kms keyrings list
 5914  gcloud kms keyrings list --location=us
 5915  gcloud kms keyrings list --location=global
 5916  gcloud kms keyrings describe --location=global
 5917  gcloud kms keyrings describe
 5918  gcloud kms keyrings describe projects/pentaho-lee-cheng/locations/us/keyRings/moseisley-us-keyring
 5919  gcloud kms keyrings describe moseisley-us-keyring
 5920  gcloud kms keyrings describe projects/pentaho-lee-cheng/locations/us/keyRings/moseisley-us-keyring/cryptoKeys/moseisley-encryted-key-1
 5921  gcloud kms keyrings describe projects/pentaho-lee-cheng/locations/us/keyRings/moseisley-us-keyring/cryptoKeys/moseisley-encrypted-key-1
 5932  gcloud iam service-accounts list
 5933  gcloud iam service-accounts describe moseisley-encryption
 5934  gcloud iam service-accounts describe moseisley-encryption@pentaho-lee-cheng.iam.gserviceaccount.com
 6045  gcloud beta compute ssh --zone "us-central1-a" "lumada-installer" --tunnel-through-iap --project "hv-gcp-trycatalog"
 6060  gcloud compute ssh --zone "us-central1-a" "installer@pikachu-installer" --tunnel-through-iap --project "hv-gcp-trycatalog"
 6527  gcloud compute config-ssh
 6833  gcloud compute health-checks list
 6834  gcloud compute health-checks delete cicd-cluster-healthcheck magneton-lb-healtcheck
 6835  gcloud compute health-checks list
 6956  gcloud compute health-checks list
 6957  gcloud compute firewall-rules list
 6975  gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:dns01-solver@$PROJECT_ID.iam.gserviceaccount.com --role roles/DNSCertVerifier
 6976  gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:dns01-solver@$PROJECT_ID.iam.gserviceaccount.com --role projects/hv-gcp-trycatalog/roles/DNSCertVerifier

 8113  gcloud services enable container.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
 8115  gcloud builds submit --tag gcr.io/${PROJECT_ID}/runner:latest .
 8116  gcloud iam service-accounts create runner-sa --display-name "runner-sa"\n
 8117  gcloud iam service-accounts list --filter="displayName:runner-sa" --format='value(email)'
 8118  SA_EMAIL=$(gcloud iam service-accounts list --filter="displayName:runner-sa" --format='value(email)')
 8119  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member serviceAccount:$SA_EMAIL --role roles/editor
 8122  gcloud iam service-accounts add-iam-policy-binding --role roles/iam.workloadIdentityUser --member "serviceAccount:${PROJECT_ID}.svc.id.goog[default/gke-runner-sa]" runner-sa@${PROJECT_ID}.iam.gserviceaccount.com