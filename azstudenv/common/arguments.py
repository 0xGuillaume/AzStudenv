"""."""
import typer
from enum import Enum
from typing import Tuple


DEBIAN = "debian"
RHEL = "rhel"
UBUNTU = "ubuntu"




class VmImages(str, Enum):
    """
    """

    debian  = DEBIAN
    rhel    = RHEL
    ubuntu  = UBUNTU


class VmAmount(str, Enum):
    """
    """
    
    one = 1
    two = 2
    three = 3



def complete_images() -> list:
    """Return list of availanle images"""

    return [DEBIAN, RHEL, UBUNTU]


app = typer.Typer()


class CliParser:
    """
    """

    def __init__(self) -> None:
        """Init CliParser class."""


    @app.command()
    def infra(amount:VmAmount = typer.Argument(VmAmount, help="Amount of virtual machines to create.", show_default=False),
            images:VmImages = typer.Argument(VmImages, help="Which image to create", show_default=False, autocompletion=complete_images),
            poc:str = typer.Argument(..., help="The name of POC.", show_default=False)
        ) -> None:
        """
        Configure Azure infrastructure : POC, Vms (amount), Images (ISO).
        """
        print(f"Configuring infrastructure")


    @app.command()
    def build() -> None:
        """
        Build Azure infrastructure using Terraform.

        Terraform command used : terraform apply --auto-approve
        """
        print(f"Building infrastructure")


    @app.command()
    def destroy() -> None:
        """
        Destroy Azure infrastructure using Terraform.

        Terraform command used : terraform destroy --auto-approve
        """
        print(f"Destroying infrastructure")



#if __name__ == "__main__":
CliParser()
app()

