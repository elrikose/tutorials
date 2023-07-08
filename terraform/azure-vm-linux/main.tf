resource "azurerm_resource_group" "vm_ubuntu" {
  name     = local.resource_group
  location = local.location
}

resource "azurerm_linux_virtual_machine" "linux_vm" {
  name                            = "linux-vm"
  resource_group_name             = local.resource_group
  location                        = local.location
  size                            = "Standard_D2s_v3"
  admin_username                  = "ubuntu"
  admin_password                  = "FooBurgerBar?!"
  disable_password_authentication = false
  network_interface_ids = [
    azurerm_network_interface.vm_interface.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  depends_on = [
    azurerm_network_interface.vm_interface
  ]
}

