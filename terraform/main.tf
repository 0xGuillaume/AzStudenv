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
		public_ip_address_id		  = azurerm_public_ip.main["${each.key}"]
	}
}

