# Azure

[Azure](https://portal.azure.com) is the Micrsoft Cloud.

# Azure CLI Commands

Authentication and Subscription management

```sh
# Login to and account
az login

# Show your current subscription
az account show --output table

# List all subscriptions
az account list -o table

# Set the subscription name
az account set --subscription "Sandbox"
```

Credentials for ACR and AKS

```sh
# Download .kube/config credentials
az aks get-credentials --name aks-sandbox --resource-group rg-sandbox

# Login to an ACR
az acr login --name acrsandboxregistry

# Push an image to the registry
podman push acrsandboxregistry.azurecr.io/my-image:v1.0.2

```

Query information

```sh
# List nodepool info
az aks nodepool list --resource-group rg-sandbox --cluster-name aks-sandbox --output table

# Get a list of VMs
az vm image list --output table
```
