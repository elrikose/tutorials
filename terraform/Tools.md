# Other Hashicorp Tools

# Packer

Packer allows you to provision build images that will be stored
- Immutable infrastructure
- Faster deploys of multiple servers
- Machine is configured with a template, provisioned with Ansible or some other config management tool.

Packer Template File
- Uses HCL
- Supports a wide variety of provisioners
  - Chef
  - Puppet
  - Ansible
  - Powershell
  - Bash
  - Salt

Referencing a Packer Image with Terraform means using a `data` source for something in the cloud, for example an AMI that you built.

# Consul

Consul is a service networking platorm.

- Service discovery
- Service mesh
- Application configuration

Useful when you have hundreds or thousands of services. Useful as a remote backend through it key value store

# Hashicorp Vault

Vault is a tool for securely accessing secrets.

Secrets engines sit on top of your vault cluster. 

- Unified secret manager to AWS, Google Cloud, Azure service principles, etc
- Tight access control 
- Credentials expire to the vault
- Audit log
- Snapshotting

# Atlantis

Atlantis is an open source tool to automate Pull Requests in your SCM. It is now maintained by Hashicorp.

# Cloud Development Kit for Terraform

The AWS CDK allows you to write Typescript, Python, Java, Go to generate CloudFormation. The CDK Terraform will instead write Terraform.

# Gruntwork

Gruntwork is a company that writes Terraform

- Infrastructure as Code Library - Code for AWS, GCP, Azure, Bash
- Terragrunt - Thing wrapper around Terraform for working with multiple Terraform modules and dealing with remote state.
- Terratest - Testing framework for Terraform
