"""."""
import os
import typer
from enum import Enum
from typing import Tuple
from rich.console import Console
from common.tf import Terraform
from common.parser import ConfigCompliant, ArgumentsCheck, ConfigSetup
from common.files import Yaml, Json


DEBIAN = "debian"
RHEL = "rhel"
UBUNTU = "ubuntu"

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
CONFIG_FILE = "terraform/config.yaml"
CONFIG = Yaml.read(CONFIG_FILE)


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



# ==================================================


app = typer.Typer()


class Args:
    """
    """

    def __init__(self, amount:str, image:str, poc:str):
        self.amount = amount
        self.image  = image
        self.poc    = poc


class CliParser:
    """
    """


    def __init__(self, app) -> None:
        """Init CliParser class."""


    @app.command()
    def infra(
        amount:VmAmount = typer.Argument(VmAmount, help="Amount of virtual machines to create.", show_default=False),
        image:VmImages = typer.Argument(VmImages, help="Which image to create", show_default=False, autocompletion=complete_images),
        poc:str = typer.Argument(..., help="The name of POC.", show_default=False)
    ) -> None:
        """
        Configure Azure infrastructure : POC, Vms (amount), Images (ISO).
        """

        if (
            not ArgumentsCheck(poc)
            or not bool(ConfigCompliant(CONFIG))
        ):
            return

        args = Args(amount.value, image.value, poc)
        config = ConfigSetup(CONFIG_FILE, CONFIG, args) 
        config.fill()


    @app.command()
    def build() -> None:
        """
        Build Azure infrastructure using Terraform.

        Terraform command used : terraform apply --auto-approve
        """

        # Config
        config = ConfigCompliant(CONFIG)
        
        if not config.is_instance():
            return

        if not Terraform.is_init():
            return

        Terraform.command("apply")


    @app.command()
    def destroy() -> None:
        """
        Destroy Azure infrastructure using Terraform.

        Terraform command used : terraform destroy --auto-approve
        """

        Terraform.command("destroy")


if __name__ == "__main__":
    app()
