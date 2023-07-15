# Infrastructure Drift

Infrastructure drift is when the resources are in a different state than the terraform state.

State can be fixed in 3 ways

- Replacing resources - When a resource is damage use the `-replace` flag
- Importing resources - Manually add a resource to the state file
- Refresh state - `-refresh-only` refreshes the manual configuration changes

# Resource Addressing

It is important for replacing or importing resources:

- `module.module_name[index]`
- `resource_type.resource_name[index]`

Indexes are when you create a `count` of more than one

# Replacing resources

You used to be able to `terraform taint azure_vm_instance.linux_vm`, but now you must use the newer `terraform apply -replace="azure_vm_instance.linux_vm"` because it asks if you want to replace the damaged object. You can't replace more than one file.

# terraform import

`terraform import` - Import existing resources into terraform
- Define a placeholder
- Leave the body blank
- Import `terraform import resource_type.resource_name foo`
- You can't import more than one in a command invocation
- Not all resources are importable.

# terraform refresh

`terraform refresh` reads the current remote objects and updates the state
- `terraform refresh` is an alias for `terraform apply -refresh-only -auto-approve`
- Deprecated for `-refresh-only`.

`-refresh-only` can be used with apply or plan to update the state without making changes to the remote infrastructure.

User scenario: An engineer manually deletes infrastructure by mistake and doesn't use terraform destroy.

- `terraform apply` will re-apply the VM (considers state file wrong)
- `terraform apply -refresh-only` will update the state that the VM is is missing. (considers state file right)