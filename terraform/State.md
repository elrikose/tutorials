# Terraform State

A particular condition of cloud resources during a specific time frame.

"A Virtual Machine running Ubuntu in Azure with a D-series"

Terraform creates a `terraform.tfstate` json file.

# terraform state

There are a number of `terraform state` commands

```sh
 list     List resources in the state
 mv       Move an item in the state
 pull     Pull current state and output to stdout
 push     Update remote state from a local state file
 rm       Remove instances from the state
 show     Show a resource in the state
```

Here is how you `list` items in the state:

```sh
$ terraform state list
azurerm_linux_virtual_machine.linux_vm
azurerm_network_interface.vm_interface
azurerm_public_ip.vm_public_ip
azurerm_resource_group.vm_ubuntu
azurerm_subnet.vm_subnet
azurerm_virtual_network.vm_network
```

And `show` the VM:

```sh
$ terraform state show azurerm_linux_virtual_machine.linux_vm
# azurerm_linux_virtual_machine.linux_vm:
resource "azurerm_linux_virtual_machine" "linux_vm" {
    admin_password                  = (sensitive value)
    admin_username                  = "ubuntu"
    allow_extension_operations      = true
    computer_name                   = "linux-vm"
    ...
    private_ip_address              = "10.0.1.4"
    private_ip_addresses            = [
        "10.0.1.4",
    ]
    public_ip_address               = "172.173.163.9"
    public_ip_addresses             = [
        "172.173.163.9",
    ]
    ..
    source_image_reference {
        offer     = "0001-com-ubuntu-server-jammy"
        publisher = "Canonical"
        sku       = "22_04-lts-gen2"
        version   = "latest"
    }
}
```

`terraform state mv` allow you to rename a resource in the state so it won't create/destroy the resource.

```sh
$ terraform state mv azurerm_linux_virtual_machine.linux_vm azurerm_linux_virtual_machine.ubuntu_vm
Move "azurerm_linux_virtual_machine.linux_vm" to "azurerm_linux_virtual_machine.ubuntu_vm"
Successfully moved 1 object(s).
```

# State backup

Anything that modifies state will create a backup file `terraform.tfstate.backup`. You can't disable this.