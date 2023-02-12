#!/bin/python3

"""."""
import os
import typer
from pathlib import Path
from common.tf import Terraform
from common.files import Yaml, Json#, Console
from common.parser import ConfigCompliant, ConfigSetup, ArgumentsCheck
from common.headers import header
from arguments import CliParser
from rich.console import Console


console = Console()


def main(config:str) -> None:
    """Main function."""


    config_compliant = bool(ConfigCompliant(CONFIG))
    tf_state = Json.read("terraform/terraform.tfstate")

    if not Terraform.has_been_destroyed(tf_state):
        console.log("[yellow]Warning - Previous infrastructure have not been destroyed.")

    if not Terraform.is_init():
        return

    if not config_compliant:
        return

    console.log("[cyan]Yaml configuration is compliant.")
    config = ConfigSetup(CONFIG_FILE, CONFIG, arguments)
    config.fill()

    CliParser(app)


if __name__ == "__main__":

    try:
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        CONFIG_FILE = "terraform/config.yaml"
        CONFIG = Yaml.read(CONFIG_FILE)
        main(CONFIG_FILE)

    except FileNotFoundError as error:
        Console.error(CONFIG_FILE, error)
