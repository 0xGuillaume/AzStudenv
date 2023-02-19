"""."""
import os
import typer
from enum import Enum
from typing import Tuple, Optional
from pathlib import Path
from rich.console import Console
from common.tf import Terraform
from common.parser import ConfigCompliant, ArgumentsCheck, ConfigSetup
from common.files import Yaml, Json
from common.config import ConfigUser, ConfigInfra


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
            not ArgumentsCheck.poc_name(poc)
            or not bool(ConfigCompliant(CONFIG))
        ):
            return

        ConfigInfra(
            amount, 
            image, 
            poc
        )

        #args = Args(amount.value, image.value, poc)
        #config = ConfigSetup(CONFIG_FILE, CONFIG, args) 
        #config.fill()


    @app.command()
    def build() -> None:
        """
        Build Azure infrastructure using Terraform.

        Terraform command used : terraform apply --auto-approve
        """

        config = ConfigCompliant(CONFIG)

        if not config.is_infra():
            return

        if not Terraform.is_init():
            return

        if not ArgumentsCheck.is_sshkey(ssh_key):
            return

        if not ArgumentsCheck.subscription(subscription):
            return

        Terraform.command("apply")


    @app.command()
    def destroy() -> None:
        """
        Destroy Azure infrastructure using Terraform.

        Terraform command used : terraform destroy --auto-approve
        """

        Terraform.command("destroy")


    @app.command()
    def config(
        subscription: str = typer.Option(..., prompt="Enter your Azure subscription ID", hide_input=True),
        ssh_key: Optional[Path] = typer.Option(..., prompt="Enter the path of your id_rsa.pub key"),
        user: str = typer.Option(..., prompt="Enter the username you would like to use"),
    ) -> None:
        """Configure : Azure subscription, ssh public key, user"""

        ConfigUser(
            subscription,
            ssh_key,
            user
        )



if __name__ == "__main__":
    app()
