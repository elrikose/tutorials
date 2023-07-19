# terraform

[Terraform](https://www.terraform.io/) is an Infrastructure as Code (IaC) tool that is agnostic to any cloud vendor. 

- It is declarative by nature, but has some imperative concepts. 
- It aspires to be idempotent, but sometimes changes cause a destruction/recreation event.
- Providers often wrap cloud APIs
- There is a [Terraform Associate](https://developer.hashicorp.com/terraform/tutorials/certification-003) certification, but currently no professional

# Topics

Basics
- [Terraform Providers](./Providers.md) - Provides shared logic such as modules
- [Terraform Provisioners](./Provisioners.md) - Provision infrastructure after it is built
- [Terraform Language](./Language.md) - Language topics (eg. variables, data)
- [Terraform Expressions](./Expressions.md) - Using expressions
- [Terraform State](./State.md) - Querying and manipulating state
- [Terraform Modules](./Modules.md) - Shared code for Terraform
- [Terraform Backends](./Backends.md) - State and operation backends
- [Terraform Workspaces](./Workspaces.md) - Workspaces

Hashicorp
- [Terraform Cloud](./Cloud.md) - Terraform Cloud
- [Terraform Enterprise](./Enterprise.md) - Terraform Enterprise
- [Other Hashicorp Tools](./Tools.md) - Packer, Consul, Vault, etc.

Fixing and troubleshooting
- [Troubleshooting](./Troubleshooting.md)
- [Infrastructure Drift](./InfrastructureDrift.md) - When remote resources drift from your terraform state

# Projects

- [Azure Linux VM](./azure-vm-linux/) - Create an Azure Linux VM


# References

Terraform
- [Terraform](https://www.terraform.io/)
- [Terraform Registry](https://registry.terraform.io/) - providers, modules

Providers
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- [GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest)
- [Kubernetes Provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest)

Azure Specific
- [Terraform Azure Examples](https://github.com/cloudxeus/terraform-azure)
- [Azure Infrastructure with Terraform](https://www.youtube.com/playlist?list=PLLc2nQDXYMHowSZ4Lkq2jnZ0gsJL3ArAw)

Certification
- [Terraform Certification from freeCodeCamp](https://www.youtube.com/watch?v=V4waklkBC38)
- [ExamPro Certification Course](https://www.exampro.co/terraform)


