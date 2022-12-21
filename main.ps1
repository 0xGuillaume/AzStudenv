#!/usr/bin/pwsh
# Az Studenv

# Parse json config file
function ConfigParser {

	$config = Get-Content "config.json" | Out-String | ConvertFrom-Json
	return $config
}



# Create Azure Resource Group
function AzResourceGroup {
	
	$name = "Mon_Super_RG"
	$resourceGroup = New-AzResourceGroup -Name $name -Location $config.Location
	
	return $resourceGroup
}


# Create Azure Virtual Network
function AzVnet {

	$vnetName = "MyVnet"
	$resourceGroup = AzResourceGroup

	$vnet = @{
		Name 				= $vnetName
		ResourceGroupName 	= $resourceGroup.ResourceGroupName
		Location 			= $config.location
		AddressPrefix 		= '10.0.0.0/16'
	}
	$virtualNetwork = New-AzVirtualNetwork @vnet

	return $virtualNetwork
}


# Create Azure Subnet
function AzSubnet {

	$subnetName = "MonSubnet"
	$virtualNetwork = AzVnet

	$subnet = @{
		Name = $subnetName
		VirtualNetwork = $virtualNetwork.Name
		AddressPrefix = "10.0.0.0/24"
	}

	#Add-AzVirtualNetworkSubnetConfig -Name $subnetName -VirtualNetwork $virtualNetwork -AddressPrefix "10.0.0.0/24"
	Add-AzVirtualNetworkSubnetConfig @subnet
	$virtualNetwork = Set-AzVirtualNetwork
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
Connect-AzAccount 
#AzResourceGroup
#AzVnet
AzSubnet
