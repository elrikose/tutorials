# CLI

Main Actions:

- `terraform init` - initialize the project. Get latest providers and modules
- `terraform fmt` - format the source code in an opinionated way
- `terraform validate` - validate types and values. required attributes are present in code
- `terraform plan` - create an execution plan, also executes `validate`
- `terraform apply` - apply the infrastructure. Use `-auto-approve` to not be prompted.
- `terraform destroy` - destroy the infrastructure

# terraform providers

Get a list of terraform providers in the local folder:

```sh
$ terraform providers

Providers required by configuration:
.
└── provider[registry.terraform.io/hashicorp/azurerm] 3.64.0
```

# terraform console

`terraform console` - A way to run ad-hoc terraform commands from variables that may be defined:

```sh
$ terraform console
> "Hello there!"
"Hello there!"
>
```

# terraform init

`terraform init`
- Downloads providers and modules
- Creates a `.terraform directory`
- Creates a dependency lock file `.terraform.lock.hcl` for plugin and terraform versions
- Modifying or changing dependencies requires a rerun of `terraform init`

`terraform init -upgrade` upgrades all of the plugins to the latest version

# terraform get

Similar to `terraform init` except only updates modules.

# terraform fmt

`terraform fmt` - Styles terraform configuration files (rewrites .tf)

# terraform validate

`terraform validate` - Validates the syntax and the arguments of the `.tf` files. `plan` and `apply` call it and will complain if there is a missing attribute.

# terraform plan

`terraform plan`
- Reads the current state to see if it needs to change
- Compares the current state and notes changes (create, update, delete, etc)
- Proposes the changes, but **doesn't** execute it.
- Terraform plan is a binary file
- You can save a plan that can be used as the input to the `terraform apply` via `terraform plan -out=my_plan.tfplan`
- Note that the saved plan will not need to be auto-approved!
# terraform apply

`terraform apply`
- Validates, executes, and apply's the plan
- Automatic plan must be manually approved by default
- `-auto-approve` approves without prompting



