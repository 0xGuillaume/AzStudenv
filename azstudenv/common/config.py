"""Module handling configuration setup."""
import re
import os
import string
from pathlib import Path
from typing import Union
from common.files import Yaml, Console


CONFIG_FILE = "/home/guillaume/projects/AzStudenv/azstudenv/terraform/config.yaml"


class ConfigTest:
    """Configurations unit tests.

    Several tests to check if configuration file
    key are compliant. 
    Those tests run before appending to the configuration file
    and before running AzStudenv commands.
    """

    def __init__(self) -> None:
        """Initialize ConfigTest class."""


    def is_username(self, username:str) -> bool:
        """Check if the given admin username is azure compliant.
        
        Args:
            username: User's given username.
        """

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
            message = (
                "Admin username value must be between 1 and 64 characters"
                f"long [Length: {len(username)}]."
            )
            Console.error(message)
            return False

        if username in banned_username:
            message = (
                f"Given admin username : [cyan bold]{username}[/cyan bold] "
                "is a banned value by Azure."
            )
            Console.error(message)
            return False

        for char in username:
            if char not in authorized_chars:
                message = (
                    f"[[cyan bold]{char}[/cyan bold] in [cyan bold]{username}[/cyan bold] "
                    "[Position: {count + 1}]"
                    "is not an authorized character for admin_username."
                )
                Console.error(message)
                return False
        return True


    def is_pocname(self, name:str) -> bool:
        """Check if poc name is alphanumeric only.

        Args:
            name: User's given proof of concept name.
        """

        if not name.isalpha():
            message = (
                f"[cyan bold]{name}[/cyan bold] is not a valid name. "
                "Only letters are allowed for naming POC."
            )
            Console.error(message)

        return name.isalpha()


    def is_subscription(self, id_:str) -> bool:
        """Check wether or not Azure subscription ID is well formatted.
        
        Args:
            id_: User's Azure subscription.
        """

        pattern = "[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}"

        if not bool(re.match(pattern, id_)):
            message = (
                f"Given Azure subscription [cyan bold]{id_}[/cyan bold] "
                "does not respect Azure subscription pattern."
            )
            Console.error(message)
            return False

        return True


    def is_sshkey(self, path:Union[str, os.PathLike]) -> bool:
        """Check wether or not ssh_key path exists.

        Args:
            path: User's ssh public key path.
        """

        if not Path(path).exists():
            message = f"SSH Public key [cyan bold]{path}[/cyan bold] does not exist."
            Console.error(message)
            return False

        return True

    def is_init(self) -> bool:
        """Check wether or not config has been init (is not empty)."""

        config = bool(Yaml.read(CONFIG_FILE))

        if not config:
            message = (
                "Configuration file [cyan bold]config.yaml[/cyan bold] " 
                "is empty or has not been set. "
                "Run [cyan bold]config[/cyan bold] command in order to initate "
                "configuration file."
            )
            Console.error(message)
            return False

        return True



class Config(ConfigTest):
    """Default configuration.

    Config is used to store default configuration
    YAML pattern and allowed images used to 
    setup instances.

    Config is also used to interact with `config.yaml` file:
        - Initiate configuration file.
        - Fill or append new configuration.
        - Reset configuration file.
    """

    def __init__(self) -> None:
        """Initialize Config clas."""

    def _default(self) -> dict:
        """Default configuration pattern."""

        default = {
            'idrsa': None, 
            'instances': None, 
            'location': 'FranceCentral', 
            'poc': None, 
            'subscription': None, 
            'suffix': None, 
            'vm': {
                'size': 'Standard_B1s',
                'admin_username': None, 
                'image': {
                    'offer': None, 
                    'publisher': None, 
                    'sku': None, 
                    'version': None
                }
            }
        }

        return default


    def _image(self) -> dict:
        """Return chosen image."""

        images = {
            'debian': {
                'offer': 'debian-11', 
                'publisher': 'debian', 
                'sku': '11', 
                'version': 'latest'
            },
            'rhel': {
                'offer': 'RHEL', 
                'publisher': 'RedHat', 
                'sku': '86-gen2', 
                'version': 
                'latest'
            },
            'ubuntu': {
                'offer': '0001-com-ubuntu-server-focal', 
                'publisher': 'canonical', 
                'sku': '20_04-lts-gen2', 
                'version': 'latest'
            }
        }

        return images


    def init(self) -> None:
        """Init configuration file with default model."""

        Yaml.write(CONFIG_FILE, self._default())


    def reset(self) -> None:
        """Reset configuration file with default model."""


    def fill_config_infra(self, instances:dict, image:str, pocname:str, suffix:str) -> None:
        """Fill the infrastructure configuration in config.yaml.
        
        Args:
            instances: Dictionnary of instances (hostname:image) to create.
            image: Detailed image (ISO) chosen.
            pocname: POC name chosen.
            suffix: 3 capital letters based on firt 3 letters of the POC name.
        """

        config = Yaml.read(CONFIG_FILE)

        config["poc"] = pocname
        config["suffix"] = suffix
        config["instances"] = instances
        config["vm"]["image"] = image

        Yaml.write(CONFIG_FILE, config)


    def fill_config_user(self, subscription:str, sshkey:str, username:str) -> None:
        """Fill User's configuration in config.yaml.
        
        Args:
            subscription: User's Azure subscription.
            sshkey: User's SSH key path.
            username: Username used by user to connect instances.
        """

        config = self._default()
        config["idrsa"] = sshkey
        config["subscription"] = subscription
        config["vm"]["admin_username"] = username

        Yaml.write(CONFIG_FILE, config)


    def is_well_formated(self) -> bool:
        """Check if configuration is well formated."""

        default = self._default()
        config = Yaml.read(CONFIG_FILE)

        main = config.keys() == default.keys()
        host = config["vm"].keys() == default["vm"].keys()
        image = config["vm"]["image"].keys() == default["vm"]["image"].keys()

        return main == host == image


    def is_compliant(self) -> bool:
        """Check if configuration is compliant."""

        #config = Yaml.read(CONFIG_FILE)
        #fmt = self.is_well_formated(config)
        return



class ConfigInfra(Config):
    """Configuration of the infrastructure to create.

    Setup the infrastructure configuration based on 
    the user choices :
        - Amount of instances.
        - Images (rhel, ubuntu, debian).
        - POC name.

    Attributes:
        amount: A string between : 1, 2 or 3.
        image: A string between : rhel, ubuntu or debian.
        pocname: A string indicating the infrastructure POC name.
    """

    def __init__(
        self,
        amount:str,
        image:str,
        pocname:str
    ) -> None:
        """Initialize ConfigInfra class.
        
        Args:
            amount: Amount of instances to create.
            image: Image on wich instances will be based.
            pocname: Name of the POC.
        """

        self.amount     = amount
        self.image      = image
        self.pocname    = pocname

        # Check if config has already been settuped by ConfigUser
        if not self.is_init():
            return

        self.fill_config_infra(
            self._instances(),
            self._image()[self.image],
            self._pocname(),
            self._suffix()
        )

        message = (
            "[green bold]✓[/green bold] [bold]"
            "Infrastructure configuration successfully setup![/bold]"
        )
        Console.info(message)


    def _pocname(self) -> str:
        """Define poc name."""

        if not self.is_pocname(self.pocname):
            return False

        return f"POC_{self.pocname.capitalize()}"


    def _suffix(self) -> str:
        """Define poc name suffix in 3 capital letters."""

        return self.pocname[:3].upper()


    def _instances(self) -> dict:
        """Set hostname and ISO image for Az virtual machines."""

        hosts = int(self.amount)
        instances = {}

        for host in range(0, hosts):
            image = self.image[:3].upper()
            instance = f"AZUX{image}0{host + 1}"
            instances[instance] = self.image.value

        return instances



class ConfigUser(Config):
    """Configuration of the user's settings.

    Setup the configuration file with required
    user's settings for Azure and Terraform needs:
        - Azure subscription.
        - SSH key path.
        - Username.

    Attributes:
        subscription: A string indicating user's Azure subscription.
        sshkey: A string indicating a SSH key path.
        username: A string indicating a username.
    """

    def __init__(
        self,
        subscription:str,
        sshkey:str,
        username:str
    ) -> None:
        """Initialize ConfigUser class.
        
        Args:
            subscription: User's Azure subcription.
            sshkey: User's sshkey path.
            username: Username used on instances (username@host).
        """

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
                _subscription,
                _sshkey,
                _username
            )

            message = (
                "[green bold]✓[/green bold] [bold]"
                "User configuration successfully filled![/bold]"
            )
            Console.info(message)


    def _username(self) -> str:
        """Define Azure VM admin username."""

        if not self.is_username(self.username):
            return False

        return self.username


    def _subscription(self) -> str:
        """Fill Azure subscription."""

        if not self.is_subscription(self.subscription):
            return False

        return self.subscription


    def _sshkey(self) -> str:
        """Fill SSH public key."""

        if not self.is_sshkey(self.sshkey):
            return False

        return str(self.sshkey)
