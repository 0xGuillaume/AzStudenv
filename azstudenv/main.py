#!/bin/python3

"""."""
import os
import argparse
from pathlib import Path
from common.tf import Terraform
from common.files import Yaml, Json, Console
from common.parser import ConfigCompliant, ConfigSetup, ArgumentsCheck


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


def main(config:str) -> None:
    """Main function."""

    arguments = args_parser()
    config_compliant = bool(ConfigCompliant(CONFIG))
    tf_state = Json.read("terraform/terraform.tfstate")

    if not config_compliant:
        return

    Console.info("Yaml configuration is compliant.")

    if not bool(ArgumentsCheck(arguments)):
        return

    config = ConfigSetup(CONFIG_FILE, CONFIG, arguments)
    config.fill()

    Console.info("Waiting for Terraform script to execute...")

    if not Terraform.has_been_destroyed(tf_state):
        return

    if not Terraform.is_init():
        return


    """
    if Terraform.apply():
        Terraform.output(tf_state)
        message = ("All Azure resources have been created. Check your"
            "Azure Portal (https://portal.azure.com/) for more details.")
        Console.info(message)
    """


if __name__ == "__main__":

    try:
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")
        CONFIG_FILE = "terraform/config.yaml"
        CONFIG = Yaml.read(CONFIG_FILE)
        main(CONFIG_FILE)
        #print(os.curdir)

        #test = Path(__file__).parent / "config.yaml"
        #print(test)

    except FileNotFoundError as error:
        Console.error(CONFIG_FILE, error)
