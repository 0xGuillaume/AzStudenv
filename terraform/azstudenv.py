"""Module AzStudenv."""
import argparse
import string
import yaml
from pathlib import Path


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


CONFIG = Yaml.read("config.yaml")["azure"]


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

    @classmethod
    def key_empty(self, key:str):
        """Check if a given Yaml Key exists."""

        if not key:
            return False

    @classmethod
    def file_exists(self, file:str):
        """Check if a given path and file exists."""

        if not Path(file).is_file(): 
            print("[ERROR] File '{file} does not exist.'")
            return False

    @classmethod
    def subscription(self):
        """Check if subscription ID has been filled."""

        if not self.key_empty():
            return False
        
    @classmethod
    def admin_username_is_valid(self):
        """Check if the given admin username is azure compliant."""
        
        username = CONFIG["vm"]["admin_username"]

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
            print(f"[ERROR] Admin username value must be between 1 and 64 characters long [Length: {len(username)}].")
            return False

        if username in banned_username:
            print(f"[ERROR] Current admin username : '{username}' is a banned value by Azure.")
            return False

        for count, char in enumerate(username):
            if char not in authorized_chars:
                print(f"[ERROR] '{char}' in '{username}' [Position: {count + 1}] is not an authorized character for admin_username.")
                return False
