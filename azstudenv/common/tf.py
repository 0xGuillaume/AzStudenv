"""."""
import subprocess
import typer
import time
from rich.progress import Progress
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from colorama import Fore
from common.files import Console
from typing import Literal


class Terraform:
    """
    .
    """

    def __init__(self) -> None:
        """Inits Terraform class."""

    
    @classmethod
    def resource_format(self, output:str) -> str:
        """"""

        output = output.split(":")[0].split(".")
        resource, id_ = output[0], output[1]

        resource = resource.replace("azurerm_", "")
        resource = resource.replace("_", " ")
        resource = resource.capitalize()

        fmt = f"{resource} - {id_}" 

        return fmt


    @classmethod
    def output_format(cls, output:str) -> str:
        """Format terraform console output."""

        output = output.split()
        resource = output[0].capitalize()

        Console.terraform(resource)


    @classmethod
    def command(self, option: Literal["apply", "destroy"]) -> None:
        """
        """

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:

            with subprocess.Popen(
                ["terraform", "-chdir=terraform/", option, "-auto-approve", "-no-color"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
            ) as process:
                task = progress.add_task(
                    description=f"{option.capitalize()}ing AzStudenv infrastructure...", 
                    total=None
                )

                for line in process.stdout:
                    line = line.decode("utf-8")

                    if "complete after" in line:
                        print(self.resource_format(line))


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
    def output(cls, tfstate:str) -> None:
        """Parse *.tfstate json file to get ressources values."""

        try:
            resources = tfstate["resources"]

        except FileNotFoundError:
            message = ("File `terraform.tfstate` not found. "
                "Enable to display SSH commands to connect to virtual machines.")
            Console.warning(message)
            return

        message = "Follow the SSH command(s) below to connect to your virtual machine(s) :\n\n"

        for resource in resources:
            if resource["type"] == "azurerm_linux_virtual_machine":
                for instance in resource["instances"]:

                    instance    = instance["attributes"]
                    hostname    = instance["computer_name"]
                    user        = instance["admin_username"]
                    ip_address  = instance["public_ip_address"]

                    message += Fore.CYAN + \
                        f"\t- {hostname} : ssh {user}@{ip_address}\n\n" + Fore.RESET

        Console.info(message)


    @classmethod
    def has_been_destroyed(cls, tfstate:str) -> bool:
        """Check wether or not previous terraform build has been destroyed"""

        ressources = tfstate["resources"]

        if ressources:
            message = "Tfstate file not empty. Make sure you destroyed your previous build."
            Console.warning(message)
            return False

        return True
