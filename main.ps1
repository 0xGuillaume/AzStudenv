#!/usr/bin/pwsh
Connect-AzAccount


# Create Azure Resource Group
function AzResourceGroup {
	
	$name_rg = "Mon_Super_RG"
	New-AzResourceGroup -Name $name_rg -Location 'FranceCentral'
	
	return $name_rg | Out-String
}


# Create Azure Virtual Network
function AzVnet {
	$vnet = @{
		Name = 'myVNet'
		ResourceGroupName = 'Mon_Super_RG'#AzResourceGroup
		Location = 'FranceCentral'
		AddressPrefix = '10.0.0.0/16'
	}
	$virtualNetwork = New-AzVirtualNetwork @vnet
}


# Create Azure Virtual Machines
function AzVm {
	New-AzVm `
		-ResourceGroupName AzResourceGroup` # | Out-String`
		-Name 'myVM' `
		-Location 'FranceCentral' `
		-VirtualNetworkName 'myVnet' `
		-SubnetName 'mySubnet' `
		-SecurityGroupName 'myNetworkSecurityGroup' `
		-PublicIpAddressName 'myPublicIpAddress' `
		-OpenPorts 80,3389
}

#AzResourceGroup
AzVnet

#Write-Host "Hello world"
