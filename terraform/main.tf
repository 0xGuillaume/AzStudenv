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


# SSH Key
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

