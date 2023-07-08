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

# App Registrations

For automation it is common that you need to create a service account that can be used to get the following 4 values:

- azure_subscription_id - Azure subscription
- azure_tenant_id - Azure tenant that owns the subscription
- azure_client_id - Azure App registration client ID
- azure_client_secret - Azure app registration secret

A service account is an app registration in Azure AD. here is the process to get all of the fields above:

- You can get the **subscription ID** and **tenant ID** by running the following after `az login`:

```sh
$ az account list -o table
Name                       CloudName    SubscriptionId                        TenantId                              State    IsDefault
-------------------------  -----------  ------------------------------------  ------------------------------------  -------  -----------
Sandbox                    AzureCloud   beefbeef-beef-beef-beef-beefbeefbeef  f00df00d-f00d-f00d-f00d-f00df00df00d  Enabled  True
```

- In Azure ID, go to App Registrations > New Registration.
- Name the App Registration and set it to a single tenant
- Click Register
- In the Overview page you should get the **client ID** from the "Application (client) ID" field.
- To create the client secret, go to Certificates & secrets. Click New client secret and add a description and expiration.
- In the Value field that is created, that is the **client secret**.

You should now have all of the fields
- Now go into the Subscription and click on the Access control (IAM) area.
- Click Add > Add role assignment
- Choose the appropriate role and click Next
- Choose Select Members and select the App Registration above.
- Click Review + assign.