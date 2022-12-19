#!/usr/bin/pwsh

# Parse json config file
function ConfigParser {

	$config = Get-Content "config.json" | Out-String | ConvertFrom-Json
	return $config
}


# Create Azure Resource Group
function AzResourceGroup {
	
	$name_rg = "Mon_Super_RG"
	New-AzResourceGroup -Name $name_rg -Location $config.Location
	
	return $name_rg | Out-String
}


# Create Azure Virtual Network
function AzVnet {

	$vnet = @{
		Name 				= 'myVNet'
		ResourceGroupName 	= AzResourceGroup
		Location 			= $config.location
		AddressPrefix 		= '10.0.0.0/16'
	}
	$virtualNetwork = New-AzVirtualNetwork @vnet
}


# Create Azure Virtual Machines
function AzVm {

	New-AzVm `
		-ResourceGroupName 		AzResourceGroup `
		-Name 					'myVM' `
		-Location 				$config.location `
		-VirtualNetworkName 	'myVnet' `
		-SubnetName 			'mySubnet' `
		-SecurityGroupName  	'myNetworkSecurityGroup' `
		-PublicIpAddressName 	'myPublicIpAddress' `
		-OpenPorts 				80,3389
}


# =======================================
# Main

$config = ConfigParser
Write-Host $config.location

#Connect-AzAccount
#AzResourceGroup
#AzVnet
