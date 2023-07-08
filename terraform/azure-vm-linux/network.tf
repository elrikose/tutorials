resource "azurerm_virtual_network" "vm_network" {
  name                = "vm-network"
  location            = local.location
  resource_group_name = azurerm_resource_group.vm_ubuntu.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "vm_subnet" {
  name                 = "vm-subnet"
  resource_group_name  = local.resource_group
  virtual_network_name = azurerm_virtual_network.vm_network.name
  address_prefixes     = ["10.0.1.0/24"]
  depends_on = [
    azurerm_virtual_network.vm_network
  ]
}

resource "azurerm_network_interface" "vm_interface" {
  name                = "vm-interface"
  location            = local.location
  resource_group_name = local.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.vm_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.vm_public_ip.id
  }

  depends_on = [
    azurerm_virtual_network.vm_network,
    azurerm_public_ip.vm_public_ip
  ]
}

resource "azurerm_public_ip" "vm_public_ip" {
  name                = "vm-public-ip"
  resource_group_name = local.resource_group
  location            = local.location
  allocation_method   = "Static"
  depends_on = [
    azurerm_resource_group.vm_ubuntu
  ]
}