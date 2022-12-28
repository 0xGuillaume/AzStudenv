"""Module AzStudenv."""
import argparse
import string
from pathlib import Path
from colorama import Fore
import subprocess
import yaml


class Console:
    """
    .
    """

    def __init__(self):
        """Inits Console class."""


    @classmethod
    def info(cls, message:str) -> None:
        """Display an informative message."""

        output = f"[INFO] [AZSTUDENV] {message}"

        return print(Fore.GREEN + output + Fore.RESET)


    @classmethod
    def error(cls, file:str, message:str) -> None:
        """Display an error message."""

        output = f"[ERROR] - {file} - {message}"

        return print(Fore.RED + output + Fore.RESET)


    @classmethod
    def terraform(cls, resource:str) -> None:
        """Display terraform message."""

        output = f"[INFO] [TERRAFORM] {resource} has been created."
     
        return print(Fore.YELLOW + output + Fore.RESET)


class Yaml:
    """Custom methods to interract with yaml files."""

    def __init__(self):
        """Inits Yaml class."""

    @classmethod
    def read(cls, file:str) -> dict:
        """Read yaml file."""

        with open(file, "r", encoding="UTF-8") as stream:
            data = yaml.safe_load(stream)

            return data


    @classmethod
    def write(cls, file:str, data:dict) -> None:
        """Write into a yaml file."""

        with open(file, "w", encoding="UTF-8") as file_:
            yaml.dump(data, file_, default_flow_style=False)



class ConfigCompliant:
    """Checks if configuration is compliant.

    Custom class with several methods to check wether or not
    yaml configuration file is well filled. Checks list :
        - SSH id_rsa key.
        - Azure student subscription.
        - Admin username compliance.

    The class returns a boolean value that indicates if
    compliant checks are successfull or not.

    The main function waits for `True` in order
    to run Terraform scripts. `False` will ask for
    the user to fix required values.
    """

    def __init__(self):
        """Init Controls class."""

        self.config_filename = "config.yaml"

        #if bool(self.__bool__):
        #    Console.info("Yaml configuration is compliant.")


    def __bool__(self) -> bool:
        """Checks all three tests"""

        subscription = self.subscription_is_valid(CONFIG["azure"]["subscription"])
        rsa = self.id_rsa_is_valid(CONFIG["azure"]["idrsa"])
        admin_username = self.admin_username_is_valid()

        return subscription and rsa and admin_username


    def key_empty(self, key:str) -> bool:
        """Check if a given Yaml Key exists."""

        if not key:
            return True
        return False


    def file_exists(self, file:str) -> bool:
        """Check if a given path and file exists."""

        if not Path(file).is_file():
            return False
        return True


    def subscription_is_valid(self, key:str) -> bool:
        """Check if subscription ID has been filled."""

        if self.key_empty(key):
            Console.error(self.config_filename, "Config key 'subscription' is empty.")
            return False
        return True


    def id_rsa_is_valid(self, key:str) -> bool:
        """Checks about ssh id_rsa key"""

        if self.key_empty(key):
            Console.error(self.config_filename, "Config key 'idrsa' is empty.")
            return False

        if not self.file_exists(key):
            Console.error(self.config_filename, f"File does not exist '{key}'")
            return False
        return True


    def admin_username_is_valid(self) -> bool:
        """Check if the given admin username is azure compliant."""

        username = CONFIG["azure"]["vm"]["admin_username"]

        authorized_chars = string.ascii_lowercase
        authorized_chars += string.ascii_uppercase
        authorized_chars += string.digits
        authorized_chars += "-_"

        banned_username = [
                "administrator", "admin", "user", "user1", "test", "user2", "test1",
                "user3", "admin1", "1", "123", "a", "actuser", "adm", "admin2", "aspnet",
                "backup", "console", "david", "guest", "john", "owner", "root", "server",
                "sql", "support", "support_388945a0", "sys", "test2", "test3", "user4", "user5"
        ]

        if len(username) < 1 or len(username) > 64:
            message = f"Admin username value must be between 1 and 64 characters long [Length: {len(username)}]."
            Console.error(self.config_filename, message)
            return False

        if username in banned_username:
            message = f"Current admin username : '{username}' is a banned value by Azure."
            Console.error(self.config_filename, message)
            return False

        for count, char in enumerate(username):
            if char not in authorized_chars:
                message = f"'{char}' in '{username}' [Position: {count + 1}] is not an authorized character for admin_username."
                Console.error(self.config_filename, message)
                return False
        return True



class ConfigSetup:
    """
    .
    """

    def __init__(self, args:object):
        """Inits ConfigSetup class."""

        self.args = args
        self.conf = CONFIG
        self.clear()

    def clear(self) -> None:
        """Clear specific YAML config keys before dumping new data in."""

        conf = self.conf
        conf["azure"]["poc"] = ""
        conf["azure"]["suffix"] = ""
        conf["azure"]["instances"] = []
        self.conf = conf

        Yaml.write(CONFIG_FILE, self.conf)
        Console.info("Clearing previous AzStudenv configuration...")

    def hostnames(self) -> dict:
        """Set hostname and ISO image for Az virtual machines."""

        images = self.args.image
        vms = int(self.args.n)
        hostnames_ = {}

        if vms == len(images):
            count = list(range(0, vms))
            indexes = [1] * vms

        elif vms > len(images):
            count = [0] * vms
            indexes = list(range(1, vms + 1))

        for vm in range(0, vms):
            image = images[count[vm]][:3].upper()
            index = indexes[vm]
            hostname = f"AZUX{image}0{index}"
            hostnames_[hostname] = images[count[vm]]

        return hostnames_


    def poc_name(self):
        """Defines the POC name for Azure resource group."""

        name = self.args.poc
        return f"POC_{name.capitalize()}"


    def suffix(self):
        """Define suffix for Azure resources based on first 3 chars of the POC name."""

        return self.args.poc[:3].upper()

    def fill(self):
        """File YAML config file with new arguments parameters."""

        self.conf["azure"]["poc"] = self.poc_name()
        self.conf["azure"]["suffix"] = self.suffix()
        self.conf["azure"]["instances"] = self.hostnames()

        Yaml.write(CONFIG_FILE, self.conf)

        vms = len(self.hostnames())
        message = f"Configuration applied for {self.poc_name()} with {vms} virtual machine(s)."
        Console.info(message)


class ArgumentsCheck:
    """Check if arguments are well formatted.
    """

    def __init__(self, args):
        """"""

        self.args = args


    def __bool__(self) -> bool:
        """"""

        return self.poc_name() and self.images_choice()


    def poc_name(self) -> bool:
        """Check if poc name is alphanumeric only."""

        name = self.args.poc

        if not name.isalpha():
            print("Seul les lettres sont acceptees")

        return name.isalpha()


    def images_choice(self) -> bool:
        """Check if number of vms match with selected ISO images."""

        images = self.args.image
        images_count = int(self.args.n)

        if len(images) == 2 and images_count == 3:
            print("Si vous souhaitez creer 3 vms, il vous faut preciser un os pour les 3 ou un os par vm")
            return False

        if len(images) > images_count:
            print("Il y a plus d'image en argument que de nombre de vm a creer")
            return False

        return True


def args_parser() -> object:
    """Set available arguments."""

    parser = argparse.ArgumentParser(
                prog = "AzStudenv",
                description = "What the programs does.",
            )

    parser.add_argument("-n",
                choices=[str(digit) for digit in range(1, 3 + 1)],
                required=True,
                help=""
            )

    parser.add_argument("-i", "--image",
                choices=["debian", "ubuntu", "rhel"],
                required=True,
                nargs="*",
                help=""
            )

    parser.add_argument("-p", "--poc",
            required=True,
            help=""
        )

    return parser.parse_args()





class Terraform:
    """
    .
    """

    def __init__(self) -> None:
        """Inits Terraform class."""

    
    @classmethod
    def output_format(self, output:str) -> str:
        """Format terraform console output."""
        
        output = output.split()
        resource = output[0].capitalize()

        Console.terraform(resource)


    def apply(self) -> None:
        """Apply terraform files."""



    @classmethod
    def is_init(self) -> bool:
        """Check wether or not Terraform has been init."""

        tf_dir = Path(".terraform/").is_dir()
        tf_lock = Path(".terraform.lock.hcl").is_file()

        if not tf_dir:
            message = "Directory not found. You probably did not run `terraform init` to initiaize the Terraform working directory"
            Console.error("./terraform", message)

        if not tf_lock:
            message = "File not found. You probably did not run `terraform init` to initiaize the Terraform working directory"
            Console.error(".terraform.lock.hcl", message)

        return tf_dir and tf_lock



def main(config:str) -> None:
    """Main function."""

    arguments = args_parser()
    config_compliant = bool(ConfigCompliant())

    if not config_compliant:
        return

    elif config_compliant:
        Console.info("Yaml configuration is compliant.")


    if not bool(ArgumentsCheck(arguments)):
        return

    config = ConfigSetup(arguments)
    config.fill()

    Console.info("Waiting for Terraform script to execute...")

    if not Terraform.is_init():
        return


    # =============================================================

    apply = subprocess.Popen(
            ["terraform", "apply", "-auto-approve", "-no-color"], 
            shell=False, stdout=subprocess.PIPE, encoding=None
    )
    
    while True:
        line = apply.stdout.readline().decode("utf-8")
        print("!!!!!!!!!!!!!!", line)
        if "Creation complete after" in line:
            Terraform.output_format(line)

        elif "Error:" in line:
            print("error")
            break

        if not line:
            break

    Console.info("All Azure resources have been created. Check your Azure Portal (https://portal.azure.com/) for more details.")


if __name__ == "__main__":

    try:
        CONFIG_FILE = "config.yaml"
        CONFIG = Yaml.read(CONFIG_FILE)
        main(CONFIG_FILE)

    except FileNotFoundError as error:
        Console.error("config.yaml", error)
