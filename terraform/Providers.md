# Terraform Providers

Providers are plugins to terraform that allow you to map to a service 

- Clouds: AWS, Azure, GCP, etc
- Saas: Github
- API: Kubernetes, Postgres

You have to have at least one provider in terraform execution. There are 3 times of providers:

- Official - From the company directly
- Verified - Up-to-date in the registry
- Community - open source

# Terraform Registry

Website where you can find, publish, or download public providers and modules.

https://registry.terraform.io


# Private Registry

Terraform Cloud allows you to have private terraform modules. 

Terraform Cloud connects to a git that hosts your modules

# Modules

Module - Files to provide functionality for the provider.
- Reduces amount of code a user has to write
- Reduces complexity
- Enforces best practices