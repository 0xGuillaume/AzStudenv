from azure.identity import AzureCliCredential, DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
import yaml
import os


with open("../config.yaml", "r", encoding="UTF-8") as stream:
    data = yaml.safe_load(stream)


#resource_client = ResourceManagementClient(credential, subscription)
#resource_groups = resource_client.resource_groups.list()


class Azure:
    """
    """

    def __init__(self):
        """Inits Azure class."""

        self.credential = AzureCliCredential()
        self.subscription = data["azure"]["subscription"]


    @classmethod
    def max_vms(self) -> None:
        """."""

        compute = ComputeManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=self.subscription
        )
            
        vms = compute.virtual_machines.list_all()


        l = []
        
        for vm in vms:
            l.append(vm.name, vm.location)


        print(l)

        



Azure.max_vms()
