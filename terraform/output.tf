# Resource group name
output "resource_group" {
	value = azurerm_resource_group.main.name
}


# Public IP adresses
output "public_ip_addresses" {
	value = {
		"user": azurerm_linux_virtual_machine.main.admin_username
	#"hostname": values(azurerm_linux_virtual_machine.main)[*].
		"ip": azurerm_linux_virtual_machine.main.public_ip_address
	}
}
