"""."""
import subprocess
import typer
from time import sleep
from rich.console import Console
from pathlib import Path
from colorama import Fore
#from common.files import Console
from typing import Literal


console = Console()


class Terraform:
    """
    .
    """


    def __init__(self) -> None:
        """Inits Terraform class."""

    
    def resource_format(self, output:str) -> str:
        """"""

        output = output.split(":")[0].split(".")
        resource, id_ = output[0], output[1]

        resource = resource.replace("azurerm_", "")
        resource = resource.replace("_", " ")
        resource = resource.capitalize()

        fmt = f"[green]✓[/green] [bold]{resource}[/bold] - {id_}"

        return fmt


    def _actions(self, option:str) -> dict:
        """"""

        actions = [
            {
                "option": "apply",
                "color": "green", 
                "action": "Created",
                "result": "built"
            },
            {
                "option": "destroy",
                "color": "red", 
                "action": "Destroyed", 
                "result": "destroyed"
            }
        ]

        return [action for action in actions if action["option"] == option][0]


    

    @classmethod
    def command(self, option: Literal["apply", "destroy"]) -> None:
        """
        """

        amount = 0
        actions = self._actions(option)

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
                        sleep(0.5)
                        message = f"{self.resource_format(line)} - {actions[option]}"
                        console.log(message)
                        amount += 1

        console.print(f"[bold green] Infrastructure successfully built! {amount} resources created")


    @classmethod
    def is_init(cls) -> bool:
        """Check wether or not Terraform has been init."""

        tf_dir = Path("terraform/.terraform/").is_dir()
        tf_lock = Path("terraform/.terraform.lock.hcl").is_file()

        if not tf_dir:
            message = ("Directory not found. You probably did not run"
                "`terraform init` to initiaize the Terraform working directory")
            Console.error("./terraform", message)

        if not tf_lock:
            message = ("File not found. You probably did not run"
                "`terraform init` to initiaize the Terraform working directory")
            Console.error(".terraform.lock.hcl", message)

        return tf_dir and tf_lock


    @classmethod
    def has_been_destroyed(cls, tfstate:str) -> bool:
        """Check wether or not previous terraform build has been destroyed"""

        ressources = tfstate["resources"]

        if ressources:
            message = "Tfstate file not empty. Make sure you destroyed your previous build."
            Console.warning(message)
            return False

        return True

tf = Terraform()
print(tf._actions("apply"))
