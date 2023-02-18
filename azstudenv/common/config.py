import re
import os
import rich
import string
from pathlib import Path
from typing import Union
#from files import Yaml, Console
from common.files import Yaml, Console


CONFIG_FILE = "/home/jimbo/projects/AzStudenv/azstudenv/terraform/config.yaml"


class ConfigTest:
    """
    """

    def __init__(self) -> None:
        """"""


    def is_username(self, username:str) -> bool:
        """Check if the given admin username is azure compliant."""

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
            Console.error(message)
            return False

        if username in banned_username:
            message = f"Given admin username : [cyan bold]{username}[/cyan bold] is a banned value by Azure."
            Console.error(message)
            return False

        for count, char in enumerate(username):
            if char not in authorized_chars:
                message = (f"[[cyan bold]{char}[/cyan bold] in [cyan bold]{username}[/cyan bold] [Position: {count + 1}]"
                    "is not an authorized character for admin_username.")
                Console.error(message)
                return False
        return True


    def is_pocname(self, name:str) -> bool:
        """Check if poc name is alphanumeric only."""

        if not name.isalpha():
            message = (f"[cyan bold]{name}[/cyan bold] is not a valid name. "
                "Only letters are allowed for naming POC.")
            Console.error(message)

        return name.isalpha()


    def is_subscription(self, id_:str) -> bool:
        """Check wether or not Azure subscription ID is well formatted"""

        pattern = "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}" 

        if not bool(re.match(pattern, id_)):
            message = f"Given Azure subscription [cyan bold]{id_}[/cyan bold] does not respect Azure subscription pattern."
            Console.error(message)
            return False

        return True


    def is_sshkey(self, path:Union[str, os.PathLike]) -> bool:
        """Check wether or not ssh_key path exists"""

        if not Path(path).exists():
            message = f"SSH Public key [cyan bold]{path}[/cyan bold] does not exist."
            Console.error(message)
            return False
        
        return True


class Config(ConfigTest):
    """
    """

    def __init__(self) -> None:
        """"""

    def _model(self) -> dict:
        """Original configuration"""

        model = {
            'azure': {
                'idrsa': None, 
                'instances': None, 
                'location': 'FranceCentral', 
                'poc': None, 
                'subscription': None, 
                'suffix': None, 
                'vm': {
                    'size': 'Standard_B1s',
                    'admin_username': None, 
                    'image': {}
                }
            }
        }

        return model


    def fill(self) -> None:
        """Fill config if it is compliant."""

        config = self._model()

        """
        config["azure"]["idrsa"] = self.sshkey
        config["azure"]["instances"] = self._instances()
        config["azure"]["poc"] = self.pocname
        config["azure"]["subscription"] = self.subscription
        config["azure"]["suffix"] = self._suffix()
        config["azure"]["vm"]["image"] = self._image()
        config["azure"]["vm"]["admin_username"] = self.username
        """


    def init(self) -> None:
        """Init configuration file with default model."""

        Yaml.write(CONFIG_FILE, self._model())


    def reset(self) -> None:
        """Reset configuration file with default model."""
    

    def fill_config_infra(self) -> None:
        """Fill the user configuration in config.yaml."""

        #Yaml.write(CONFIG_FILE)


    def fill_config_user(self, subscription:str, sshkey:str, username:str) -> None:
        """Fill the infrastructure configuration in config.yaml."""

        config = self._model()
        config["azure"]["idrsa"] = sshkey
        config["azure"]["subscription"] = subscription
        config["azure"]["vm"]["admin_username"] = username

        Yaml.write(CONFIG_FILE, config)



class ConfigInfra(Config):
    """"""

    def __init__(
        self, 
        amount:str, 
        image:str, 
        pocname:str
    ) -> None:
        """Inits ConfigInfra class."""

        self.amount     = amount
        self.image      = image
        self.pocname    = pocname


    def _image(self) -> dict:
        """Return chosen image"""

        images = {
            'debian': {'offer': 'debian-11', 'publisher': 'debian', 'sku': '11', 'version': 'latest'}, 
            'rhel': {'offer': 'RHEL', 'publisher': 'RedHat', 'sku': '86-gen2', 'version': 'latest'}, 
            'ubuntu': {'offer': '0001-com-ubuntu-server-focal', 'publisher': 'canonical', 'sku': '20_04-lts-gen2', 'version': 'latest'}
        }

        return images[self.image]


    def _pocname(self) -> str:
        """Define poc name"""

        if not self.is_pocname(self.pocname):
            return False

        return self.pocname
        

    def _suffix(self) -> str:
        """Define poc name suffix in 3 capital letters."""

        return self.pocname[:3].upper()


    def _instances(self) -> dict:
        """Set hostname and ISO image for Az virtual machines."""

        vms = int(self.amount)
        instances = {}

        for vm in range(0, vms):
            image = self.image[:3].upper()
            instance = f"AZUX{image}0{vm + 1}"
            instances[instance] = self.image

        return instances



class ConfigUser(Config):
    """
    """

    def __init__(
        self, 
        subscription:str, 
        sshkey:str, 
        username:str
    ) -> None:
        """Inits ConfigUser class."""

        self.subscription   = subscription
        self.sshkey         = sshkey
        self.username       = username

        _subscription   = self._subscription() 
        _sshkey         = self._sshkey()
        _username       = self._username()

        if (
            _username 
            and _sshkey
            and _subscription
        ):
            if not Yaml.read(CONFIG_FILE):
                self.init()

            self.fill_config_user(
                _subscription, #self.sshkey, 
                _sshkey, #self.subscription, 
                _username#self.username
            )

            Console.info("User configuration successfully filled.")


    def _username(self) -> str:
        """Define Azure VM admin username"""

        if not self.is_username(self.username):
            return False
    
        return self.username

                        
    def _subscription(self) -> str:
        """Fill Azure subscription"""

        if not self.is_subscription(self.subscription):
            return False

        return self.subscription


    def _sshkey(self) -> str:
        """Fill SSH public key"""

        if not self.is_sshkey(self.sshkey):
            return False

        print(self.sshkey)
        print(type(self.sshkey))
        
        return str(self.sshkey)






if __name__ == "__main__":

    ConfigUser(
        "00000000-1234-0000-0000-000000000000", 
        "/home/guillaume/.ssh/id_rsa.pub",
        "jimbo"
    )

    """
    i = ConfigInfra(
        "2",
        "rhel", 
        "ansible"
    )
    """

    #r = Config()
    #r.init()

    #a = Yaml.read(CONFIG_FILE)
    #print(a)
