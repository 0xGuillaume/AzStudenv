"""."""
import string
from pathlib import Path
from common.files import Yaml, Console


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

    def __init__(self, config:dict):
        """Init Controls class."""

        self.config_filename = "config.yaml"
        self.config = config


    def __bool__(self) -> bool:
        """Checks all three tests"""

        subscription = self.subscription_is_valid(self.config["azure"]["subscription"])
        rsa = self.id_rsa_is_valid(self.config["azure"]["idrsa"])
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

        username = self.config["azure"]["vm"]["admin_username"]

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
            message = ("Admin username value must be between 1 and 64 characters"
                f"long [Length: {len(username)}].")
            Console.error(self.config_filename, message)
            return False

        if username in banned_username:
            message = f"Current admin username : '{username}' is a banned value by Azure."
            Console.error(self.config_filename, message)
            return False

        for count, char in enumerate(username):
            if char not in authorized_chars:
                message = (f"'{char}' in '{username}' [Position: {count + 1}]"
                    "is not an authorized character for admin_username.")
                Console.error(self.config_filename, message)
                return False
        return True



class ConfigSetup:
    """
    .
    """

    def __init__(self, config_filename:str, config:dict, args:object):
        """Inits ConfigSetup class."""

        self.args = args
        self.conf = config
        self.config_filename = config_filename
        self.clear()

    def clear(self) -> None:
        """Clear specific YAML config keys before dumping new data in."""

        conf = self.conf
        conf["azure"]["poc"] = ""
        conf["azure"]["suffix"] = ""
        conf["azure"]["instances"] = []
        self.conf = conf

        Yaml.write(self.config_filename, self.conf)
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

        for vm_ in range(0, vms):
            image = images[count[vm_]][:3].upper()
            index = indexes[vm_]
            hostname = f"AZUX{image}0{index}"
            hostnames_[hostname] = images[count[vm_]]

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

        Yaml.write(self.config_filename, self.conf)

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
            message = (f"'{name}' is not a valid name. "
                "Only letters are allowed for naming POC.")
            Console.argument(message)

        return name.isalpha()


    def images_choice(self) -> bool:
        """Check if number of vms match with selected ISO images."""

        images = self.args.image
        images_count = int(self.args.n)

        if len(images) == 2 and images_count == 3:
            message = ("When you create 3 vms you must specify one same image "
                "for all three of them or one image by vm.")
            Console.argument(message)
            return False

        if len(images) > images_count:
            message = (f"There are more images specified ({len(images)}) "
                    f"rather than vm to create ({images_count}).")
            Console.argument(message)
            return False

        return True
