#!/bin/python3

"""."""
import os
import argparse
from pathlib import Path
from common.tf import Terraform
from common.files import Yaml, Json, Console
from common.parser import ConfigCompliant, ConfigSetup, ArgumentsCheck
from common.headers import header
from common.arguments import CliParser, cli


def main(config:str) -> None:
    """Main function."""

    CliParser("test", "test", "test")

    header()
    config_compliant = bool(ConfigCompliant(CONFIG))
    tf_state = Json.read("terraform/terraform.tfstate")


    if not Terraform.has_been_destroyed(tf_state):
        return

    if not Terraform.is_init():
        return

    if not config_compliant:
        return

    Console.info("Yaml configuration is compliant.")

    #config = ConfigSetup(CONFIG_FILE, CONFIG, arguments)
    #config.fill()

    Console.info("Waiting for Terraform script to execute...")

    if Terraform.apply():
        tf_state = Json.read("terraform/terraform.tfstate")
        Terraform.output(tf_state)
        message = ("All Azure resources have been created. Check your"
            "Azure Portal (https://portal.azure.com/) for more details.")
        Console.info(message)


if __name__ == "__main__":

    try:
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        CONFIG_FILE = "terraform/config.yaml"
        CONFIG = Yaml.read(CONFIG_FILE)
        main(CONFIG_FILE)

    except FileNotFoundError as error:
        Console.error(CONFIG_FILE, error)
