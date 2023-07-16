# Terraform Modules

Terraform public modules can be found at the Registry: https://registry.terraform.io

Terraform private modules can be found in Terraform Cloud or corporate registries

Search only finds Official and Verified modules

# Using Modules

Terraform Registry is directly tied into terraform and is referenced as `<namespace>/<name>/<provider>`:

```js
module "consul" {
    source = hashicorp/consul/aws
    version = "0.2.0"
}
```

`terraform init` downloads any modules in the configuration

Private modules must include the host when referencing `<host>/<namespace>/<name>/<provider>`:

```js
module "mymodule" {
    source = app.terraform.io/mycomp/myname/provider
    version = "0.3.0"
}
```

You have to authenticate to private registries with `terraform login` or you can create a token and specify in the CLI config

# Publishing Modules

When you publish to the public registry you get these benefits:

- Versioning
- Version Histories
- Documentation Generation
- READMEs
- Examples

The modules have to be hosted on Github as public with a specific repo naming convention of `terraform-<PROVIDER>-<NAME>` (ie. terraform-aws-vpc)

In Terraform you have to signin to your Github account and then you push updates to the registry by using Github tags.

# Verified Modules

Verified modules
- Reviewed by Hashicorp
- Actively maintained by multiple people
- Stay up-to-date with Terraform and the dependent providers
- Get a checkmark in the Terraform registry

Unverified modules
- Isn't created by a Hashicorp partner
- Shouldn't be assumed to be poor quality

# Module Structure

There is a standard structure for files and directories:

```sh
main.tf
variables.tf
outputs.tf
README.md
LICENSE
modules/
modules/nestedModule1
modules/nestedModule2
examples/
examples/example1
examples/example2
```

- You don't need to use nested modules.
- A submodule without a README is considered internal use only