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
  config = yamldecode(file("./config.yaml"))
  image  = yamldecode(file("./config.yaml"))["vm"]["image"]
}


# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  subscription_id = ""
}


# Resource Group 
resource "azurerm_resource_group" "main" {
  name     = local.config["poc"]
  location = local.config["location"]
}


# SSH Key
resource "azurerm_ssh_public_key" "main" {
  for_each            = tomap(local.config.instances)
  name                = "${each.key}_SSHKey"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  public_key          = file(local.config["idrsa"])
}


# Virtual Machines
resource "azurerm_linux_virtual_machine" "main" {
  for_each            = tomap(local.config.instances)
  name                = each.key
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = local.config["vm"]["size"]
  admin_username      = local.config["vm"]["admin_username"]
  network_interface_ids = [
    azurerm_network_interface.main["${each.key}"].id
  ]

  computer_name                   = each.key
  disable_password_authentication = true

  source_image_reference {
    publisher = local.image["publisher"]
    offer     = local.image["offer"]
    sku       = local.image["sku"]
    version   = local.image["version"]
  }

  admin_ssh_key {
    username   = local.config["vm"]["admin_username"]
    public_key = file(local.config["idrsa"])
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  connection {
    type        = "ssh"
    user        = local.config["vm"]["admin_username"]
    host        = self.public_ip_address
    private_key = "${file("/home/jimbo/.ssh/id_rsa")}" #"${local.config["idrsa"]}"
    timeout     = "2m"
  }

  provisioner "file" {
    source      = "./scripts/setup.sh"
    destination = "/home/${local.config["vm"]["admin_username"]}/setup.sh"
  }

  provisioner "file" {
    source      = "./scripts/.vimrc"
    destination = "/home/${local.config["vm"]["admin_username"]}/.vimrc"
  }

  provisioner "file" {
    source      = "./scripts/motd"
    destination = "/tmp/motd"
  }

 provisioner "remote-exec" {
    inline = [
     "bash /home/${local.config["vm"]["admin_username"]}/setup.sh"
    ]
  }
}

