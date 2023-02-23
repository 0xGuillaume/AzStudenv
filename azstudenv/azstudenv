#!/usr/bin/env python3
"""Module handling program arguments."""
from enum import Enum
from typing import Optional
from pathlib import Path
import typer
from common.tf import Terraform
from common.config import ConfigUser, ConfigInfra, Config


app = typer.Typer()


class VmImages(str, Enum):
    """Set of choice for `--image` argument."""

    DEBIAN  = "debian"
    RHEL    = "rhel"
    UBUNTU  = "ubuntu"



class VmAmount(str, Enum):
    """Set of choice for `--amount` argument."""

    ONE     = 1
    TWO     = 2
    THREE   = 3



@app.command()
def infra(
    amount:VmAmount = typer.Argument(
        VmAmount,
        help="Amount of virtual machines to create.",
        show_default=False
    ),
    image:VmImages = typer.Argument(
        VmImages,
        help="Which image to create",
        show_default=False,
    ),
    poc:str = typer.Argument(
        ..., help="The name of POC.", show_default=False
    )
) -> None:
    """Configure Azure infrastructure : POC, Vms (amount), Images (ISO).
    
    Args:
        amount: String value between: 1, 2 or 3.
        image: String vlaue between: debian, rhel or ubuntu.
        poc: Given POC name.
    """

    ConfigInfra(
        amount,
        image,
        poc
    )


@app.command()
def build() -> None:
    """
    Build Azure infrastructure using Terraform.

    Terraform command used : terraform apply --auto-approve
    """

    config = Config()

    if not config.is_init():
        return

    if config.is_well_formated():
        Terraform.command("apply")


@app.command()
def destroy() -> None:
    """
    Destroy Azure infrastructure using Terraform.

    Terraform command used : terraform destroy --auto-approve
    """

    config = Config()

    if not config.is_init():
        return

    Terraform.command("destroy")


@app.command()
def config(
    subscription: str = typer.Option(
        ..., prompt="Enter your Azure subscription ID", hide_input=True
    ),
    ssh_key: Optional[Path] = typer.Option(
        ..., prompt="Enter the path of your id_rsa.pub key"
    ),
    user: str = typer.Option(
        ..., prompt="Enter the username you would like to use"
    )
) -> None:
    """Configure AzStudenv user's settings.

    Args:
        subscription: User's Azure subcription.
        ssh_key: User's SSH public key path.
        user: Username used to connect to instances.
    """

    ConfigUser(
        subscription,
        ssh_key,
        user
    )



if __name__ == "__main__":
    app()
