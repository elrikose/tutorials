# terraform

[Terraform](https://www.terraform.io/) is an Infrastructure as Code (IaC) tool that is agnostic to any cloud vendor. 

- It is declarative by nature, but has some imperative concepts. 
- It aspires to be idempotent, but sometimes changes cause a destruction/recreation event.
- Providers often wrap cloud APIs
- There is a [Terraform Associate](https://developer.hashicorp.com/terraform/tutorials/certification-003) certification, but currently no professional

# Projects

- [Azure Linux VM](./azure-vm-linux/) - Create an Azure Linux VM
# References

Terraform
- [Terraform](https://www.terraform.io/)
- [Terraform Registry](https://registry.terraform.io/) - providers, modules
- [Terraform Azure Examples](https://github.com/cloudxeus/terraform-azure)

Providers
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest)
- [GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest)
- [Kubernetes Provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest)

Certification
- [Terraform Certification from freeCodeCamp](https://www.youtube.com/watch?v=V4waklkBC38)
- [ExamPro Certification Course](https://www.exampro.co/terraform)

# CLI

Main Actions

- `terraform init` - initialize the project. Get latest providers and modules
- `terraform fmt` - format the source code in an opinionated way
- `terraform validate` - validate types and values. required attributes are present in code
- `terraform plan` - create an execution plan
- `terraform apply` - apply the infrastructure. Use `-auto-approve` to not be prompted.
- `terraform destroy` - destroy the infrastructure

# Terraform Provisioners

