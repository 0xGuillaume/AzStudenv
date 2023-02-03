"""."""
import argparse
import typer
from typing import Tuple
from files import Yaml


app = typer.Typer()


class CliParser:
    """
    """

    def __init__(self) -> None:
        """Init CliParser class."""


    @app.command()
    def infra(amount:int = typer.Argument(..., help="Amount of virtual machines to create.", show_default=False),
            images:str = typer.Argument(("debian", "rhel", "ubuntu"), help="Which image to create."),
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

