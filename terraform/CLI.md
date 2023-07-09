# CLI

Main Actions:

- `terraform init` - initialize the project. Get latest providers and modules
- `terraform fmt` - format the source code in an opinionated way
- `terraform validate` - validate types and values. required attributes are present in code
- `terraform plan` - create an execution plan, also executes `validate`
- `terraform apply` - apply the infrastructure. Use `-auto-approve` to not be prompted.
- `terraform destroy` - destroy the infrastructure

Get a list of terraform providers in the local folder:

```sh
$ terraform providers

Providers required by configuration:
.
└── provider[registry.terraform.io/hashicorp/azurerm] 3.64.0
``