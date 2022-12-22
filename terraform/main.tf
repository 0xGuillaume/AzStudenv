terraform {
	required_providers {
		azurerm = {
			source  = "hashicorp/azurerm"
			version = "=3.0.0"
		}
	}
}


# Locals Variable : Load config file
locals {
	config = yamldecode(file("./config.yaml"))["azure"]
	image = yamldecode(file("./config.yaml"))["azure"]["vm"]["images"]
}


# Configure the Microsoft Azure Provider
provider "azurerm" {
	features {}
		subscription_id = ""
}


# Resource Group 
resource "azurerm_resource_group" "main" {
	#for_each 			= toset(["Mon_RG_01", "Mon_RG_02", "Mon_RG_03"])
	name 				= local.config["poc"]
	location 			= local.config["location"]
}


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
	for_each 			= toset(local.config.instances)
	name                = "${each.key}_PublicIP"
	location            = azurerm_resource_group.main.location
	resource_group_name = azurerm_resource_group.main.name
	allocation_method   = "Dynamic"
}


# Create Network Security Group and Rules
resource "azurerm_network_security_group" "main" {
	name 				= "${local.config["suffix"]}_NSG"
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
	for_each 			= toset(local.config.instances)
	name                = "${each.key}_NIC"
	location            = azurerm_resource_group.main.location
	resource_group_name = azurerm_resource_group.main.name

	ip_configuration {
		name                          = "internal"
		subnet_id                     = azurerm_subnet.main.id
		private_ip_address_allocation = "Dynamic"
		public_ip_address_id		  = azurerm_public_ip.main["${each.key}"].id
	}
}


# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "main" {
	for_each 					= toset(local.config.instances)
	network_interface_id      	= azurerm_network_interface.main["${each.key}"].id
	network_security_group_id 	= azurerm_network_security_group.main.id
}


resource "azurerm_ssh_public_key" "example" {
	for_each			= toset(local.config.instances)
	name                = "${each.key}_SSHKey"
	resource_group_name   = azurerm_resource_group.main.name
	location              = azurerm_resource_group.main.location
	public_key          = file(local.config["idrsa"])
}


# Virtual Machines
resource "azurerm_linux_virtual_machine" "main" {
	for_each 			  = toset(local.config.instances)
	name                  = each.key
	resource_group_name   = azurerm_resource_group.main.name
	location              = azurerm_resource_group.main.location
	size               	  = local.config["vm"]["size"]
	admin_username 		  = local.config["vm"]["admin_username"]
	network_interface_ids = [
		azurerm_network_interface.main["${each.key}"].id
	]

	#delete_os_disk_on_termination = true
	#delete_data_disks_on_termination = true

	computer_name  = "${each.key}"
	disable_password_authentication = true

	source_image_reference {
		publisher = local.image["debian"]["publisher"] 
		offer     = local.image["debian"]["offer"]
		sku       = local.image["debian"]["sku"]
		version   = local.image["debian"]["version"]
	}

	admin_ssh_key {
		username 	= local.config["vm"]["admin_username"]
		public_key  = file(local.config["idrsa"])
	}

	os_disk {
		caching = "ReadWrite"
		storage_account_type = "Standard_LRS"
	}
}

