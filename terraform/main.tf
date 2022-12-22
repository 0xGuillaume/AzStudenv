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


# Virtual Machines
resource "azurerm_virtual_machine" "main" {
	for_each 			= toset(local.config.instances)
	name                  = each.key
	location              = azurerm_resource_group.main.location
	resource_group_name   = azurerm_resource_group.main.name
	network_interface_ids = [azurerm_network_interface.main["${each.key}"].id]
	vm_size               = local.config["vm"]["size"]["linux"]

	delete_os_disk_on_termination = true
	delete_data_disks_on_termination = true

	storage_image_reference {
		publisher = local.image["debian"]["publisher"] 
		offer     = local.image["debian"]["offer"]
		sku       = local.image["debian"]["sku"]
		version   = local.image["debian"]["version"]
	}

	storage_os_disk {
		name              = "disk_static_1"
		caching           = "ReadWrite"
		create_option     = "FromImage"
		managed_disk_type = "Standard_LRS"
	}

	os_profile {
		computer_name  = "${each.key}"
		admin_username = "user"
		admin_password = "password"
		# custom_data    = data.template_file.frontend_static_1.rendered
	}

	os_profile_linux_config {
		disable_password_authentication = false
	}
}

