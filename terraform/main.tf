terraform {
	required_providers {
		azurerm = {
			source  = "hashicorp/azurerm"
			version = "=3.0.0"
		}
	}
}

locals {
	config = yamldecode(file("./config.yaml"))["azure"]
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
	features {}
		subscription_id = ""
}

# Resource Group 
resource "azurerm_resource_group" "rgs" {
	#for_each = toset(["Mon_RG_01", "Mon_RG_02", "Mon_RG_03"])
	for_each = toset(local.config.instances)
	name     = each.key
	location = local.config["location"]
}
