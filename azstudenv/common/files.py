"""Module handling file actions."""
import json
import yaml
from rich.console import Console


console = Console()


class Yaml:
    """Custom methods to interract with yaml files."""

    def __init__(self):
        """Inits Yaml class."""

    @classmethod
    def read(cls, file:str) -> dict:
        """Read yaml file and get content.
        
        Args:
            file: File's path to read.
        """

        with open(file, "r", encoding="UTF-8") as stream:
            data = yaml.safe_load(stream)

            return data


    @classmethod
    def write(cls, file:str, data:dict) -> None:
        """Write into a yaml file.

        Args:
            file: File's path to write into.
            data: Data to write into target file.
        """

        with open(file, "w", encoding="UTF-8") as file_:
            yaml.dump(data, file_, default_flow_style=False)



class Json:
    """Custom methods to interract with json files."""

    def __init__(self):
        """Inits Json class."""

    @classmethod
    def read(cls, file:str) -> dict:
        """Read json file.

        Args:
            file: File's path to read.
        """

        with open(file, "r", encoding="UTF-8") as file_:
            data = json.load(file_)

        return data


class Console:
    """Handling console output.

    Several methods to custom output console:
        - INFO
        - ERROR
        - WARNING
    """


    def __init__(self):
        """Initialize Console class."""


    @classmethod
    def info(cls, message:str) -> None:
        """Display an informative message.

        Args:
            message: Content of the log message.
        """

        output = f"[cyan][INFO] [AZSTUDENV] {message}"

        return console.log(output)


    @classmethod
    def error(cls, message:str) -> None:
        """Display an error message.

        Args:
            message: Content of the log message.
        """

        output = f"[red][ERROR] - {message}"

        return console.log(output)


    @classmethod
    def warning(cls, message:str) -> None:
        """Display a warning message.

        Args:
            message: Content of the log message.
        """

        output = f"[yellow][WARN] [TERRAFORM] {message}"

        return console.log(output)
