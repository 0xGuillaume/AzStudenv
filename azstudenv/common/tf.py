"""."""
import subprocess
from pathlib import Path
from colorama import Fore
from common.files import Console


class Terraform:
    """
    .
    """

    def __init__(self) -> None:
        """Inits Terraform class."""


    @classmethod
    def output_format(cls, output:str) -> str:
        """Format terraform console output."""

        output = output.split()
        resource = output[0].capitalize()

        Console.terraform(resource)


    @classmethod
    def apply(cls) -> bool:
        """Apply terraform files."""

        apply = subprocess.Popen(
                ["terraform", "-chdir=terraform/", "apply", "-auto-approve", "-no-color"],
                shell=False, stdout=subprocess.PIPE, encoding=None
        )

        count = 0
        while True:
            line = apply.stdout.readline().decode("utf-8")

            if not line and not count:
                message = "Terraform error while executing. Refer to the error message above."
                Console.error("*.tf", message)
                return False

            if not line and count:
                break

            if "Creation complete after" in line:
                Terraform.output_format(line)

            count += 1

        return True

    
    @classmethod
    def destroy(cls):
        """Destroy current AzStudenv infrastructure"""

        destroy = subprocess.Popen(
                ["terraform", "-chdir=terraform/", "destroy", "-auto-approve", "-no-color"],
                shell=False, stdout=subprocess.PIPE, encoding=None
        )

        return True




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
