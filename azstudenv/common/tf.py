"""Module handling Terraform commands."""
import subprocess
from time import sleep
from pathlib import Path
from typing import Literal
from rich.console import Console


console = Console()


class Terraform:
    """Terraform commands and options.

    Formatting Terraform console output
    and methods handling Terraform commands
    `apply` and `destroy`.

    Also running tests on Terraform environment
    such as : Has been TF initialize.
    """


    def __init__(self) -> None:
        """Initialize Terraform class."""


    @classmethod
    def _actions(cls, option:str) -> dict:
        """Actions paramaters for Terraform commands.
        
        Args:
            option: Terraform command `apply` or `destroy`.
        """

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
        """Formatting Terraform output into readable text.

        Args:
            output: Terraform default console output.
            action: `apply` or `destroy` paramaters.
        """

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
    def command(self, option: Literal["apply", "destroy"]) -> None:
        """Running Terraform command in a subprocess
        and capture the output which is going to be formatted.

        Args:
            option: `apply` or `destroy` paramaters.
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

        message = (
            f"[bold green]Infrastructure successfully {action['result']}! "
            "{amount} resources {action['state']}."
        )
        console.print(message)


    @classmethod
    def is_init(cls) -> bool:
        """Check wether or not Terraform has been init."""

        tf_dir = Path("terraform/.terraform/").is_dir()
        tf_lock = Path("terraform/.terraform.lock.hcl").is_file()

        if not tf_dir:
            message = (
                "[cyan italic].terraform/[/cyan italic] directory not found. "
                "You probably did not run `terraform init` "
                "to initiaize the Terraform working directory."
            )
            console.log(f"[red bold]ERROR: {message}")

        if not tf_lock:
            message = (
                "[cyan italic].terraform.lock.hcl[/cyan italic] file not found. "
                "You probably did not run `terraform init` "
                "to initiaize the Terraform working directory."
            )
            console.log(f"[red bold]ERROR: {message}")

        return tf_dir and tf_lock
