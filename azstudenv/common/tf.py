"""."""
import subprocess
import typer
from time import sleep
from rich.console import Console
from rich.pretty import pprint
from rich.syntax import Syntax
from rich import print_json
from rich import inspect
from pathlib import Path
from typing import Literal
from common.files import Json


console = Console()


class Terraform:
    """
    .
    """


    def __init__(self) -> None:
        """Inits Terraform class."""


    @classmethod
    def _actions(cls, option:str) -> dict:
        """"""

        actions = [
            {
                "option": "apply",
                "color": "green", 
                "state": "created",
                "result": "built"
            },
            {
                "option": "destroy",
                "color": "red", 
                "state": "destroyed", 
                "result": "destroyed"
            }
        ]

        return [action for action in actions if action["option"] == option][0]
    

    @classmethod
    def resource_format(cls, output:str, action:str) -> str:
        """"""

        output = output.split(":")[0].split(".")
        resource, id_ = output[0], output[1]

        resource = resource.replace("azurerm_", "")
        resource = resource.replace("_", " ")
        resource = resource.capitalize()

        color = action["color"]
        state = action["state"].capitalize()

        fmt = f"[{color}]✓[/{color}] [bold]{resource}[/bold] - {id_} ... [bold {color}]{state}."

        return fmt


    @classmethod
    def command(cls, option: Literal["apply", "destroy"]) -> None:
        """
        """

        amount = 0
        action = self._actions(option)

        with console.status(
            f"[magenta]{option.capitalize()}ing AzStudenv infrastructure...", 
            spinner="bouncingBar"
        ) as status:

            with subprocess.Popen(
                ["terraform", "-chdir=terraform/", option, "-auto-approve", "-no-color"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
            ) as process:

                for line in process.stdout:
                    line = line.decode("utf-8")

                    if "complete after" in line:
                        sleep(1)
                        message = self.resource_format(line, action)
                        console.log(message)
                        amount += 1

        console.print(
            f"[bold green]Infrastructure successfully {action['result']}! {amount} resources {action['state']}."
        )


    @classmethod
    def is_init(cls) -> bool:
        """Check wether or not Terraform has been init."""

        tf_dir = Path("terraform/.terraform/").is_dir()
        tf_lock = Path("terraform/.terraform.lock.hcl").is_file()

        if not tf_dir:
            message = ("[cyan italic].terraform/[/cyan italic] directory not found. You probably did not run "
                "`terraform init` to initiaize the Terraform working directory")
            console.log(f"[red bold]ERROR: {message}")

        if not tf_lock:
            message = ("[cyan italic].terraform.lock.hcl[/cyan italic] file not found. You probably did not run "
                "`terraform init` to initiaize the Terraform working directory")
            console.log(f"[red bold]ERROR: {message}")

        return tf_dir and tf_lock


    @classmethod
    def has_been_destroyed(cls, tfstate:str) -> bool:
        """Check wether or not previous terraform build has been destroyed"""

        ressources = tfstate["resources"]

        if ressources:
            message = "Tfstate file not empty. Make sure you destroyed your previous build."
            console.log(f"[yellow]Warning - {message}")
            return False

        return True
