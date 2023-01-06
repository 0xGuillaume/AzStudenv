import json
import yaml
from colorama import Fore


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



class Json:
    """Custom methods to interract with json files."""

    def __init__(self):
        """Inits Json class."""

    @classmethod
    def read(cls, file:str) -> dict:
        """Read json file."""

        with open(file, "r", encoding="UTF-8") as file_:
            data = json.load(file_)

        return data


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
    def warning(cls, message:str) -> None:
        """Display a warning message."""

        output = f"[WARN] [TERRAFORM] {message}"

        return print(Fore.YELLOW + output + Fore.RESET)


    @classmethod
    def terraform(cls, resource:str) -> None:
        """Display terraform message."""

        output = f"[INFO] [TERRAFORM] {resource} has been created."

        return print(Fore.YELLOW + output + Fore.RESET)


    @classmethod
    def argument(cls, message:str) -> None:
        """Handle error during argument parsing."""

        output = f"[ARGUMENTS] {message}"

        return print(Fore.MAGENTA + output + Fore.RESET)
