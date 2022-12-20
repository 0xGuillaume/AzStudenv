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

	$name_vnet = "MyVnet"
	$vnet = @{
		Name 				= $name_vnet
		ResourceGroupName 	= AzResourceGroup
		Location 			= $config.location
		AddressPrefix 		= '10.0.0.0/16'
	}
	$virtualNetwork = New-AzVirtualNetwork @vnet

	return $name_vnet | Out-String
}


# Create Azure Subnet
function AzSubnet {
}

# Create Azure Network Interface
function AzNetworkInterface {
}

# Create Azure Public Ip Address
function AzPublicIpAddress {
}


# Create Azure Virtual Machines
function AzVm {

	New-AzVm `
		-ResourceGroupName AzResourceGroup `
		-Name 'myVM' `
		-Location $config.location `
		-VirtualNetworkName	AzVnet
		-SubnetName 'mySubnet' `
		-SecurityGroupName 'myNetworkSecurityGroup' `
		-PublicIpAddressName 'myPublicIpAddress' `
		-OpenPorts 22, 80
}


# =======================================
# Main

$config = ConfigParser
Write-Host $config.location

#Connect-AzAccount
#AzResourceGroup
#AzVnet
