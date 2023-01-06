# Azure dedicated network resources

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "${local.config["suffix"]}_VNET"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}


# Subnet
resource "azurerm_subnet" "main" {
  name                 = "${local.config["suffix"]}_SUBNET"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.0.0/24"]
}


# Public IP Addresses
resource "azurerm_public_ip" "main" {
  for_each            = tomap(local.config.instances)
  name                = "${each.key}_PublicIP"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Dynamic"
}


# Create Network Security Group and Rules
resource "azurerm_network_security_group" "main" {
  name                = "${local.config["suffix"]}_NSG"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}


# Network Interface Cards
resource "azurerm_network_interface" "main" {
  for_each            = tomap(local.config.instances)
  name                = "${each.key}_NIC"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main["${each.key}"].id
  }
}


# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "main" {
  for_each                  = tomap(local.config.instances)
  network_interface_id      = azurerm_network_interface.main["${each.key}"].id
  network_security_group_id = azurerm_network_security_group.main.id
}
