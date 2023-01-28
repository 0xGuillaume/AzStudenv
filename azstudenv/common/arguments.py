"""."""
import argparse


class ArgsParser:
    """."""

    def __init__(self):
        parser = argparse.ArgumentParser()

        self.subparser = parser.add_subparsers(help="Commands")

        apply = self.subparser.add_parser("apply")
        apply.set_defaults(func=print("Applying..."))

        destroy = self.subparser.add_parser("destroy")
        destroy.set_defaults(func=print("Destroying..."))

        build = self.subparser.add_parser("build")

        build.add_argument(
            "-i", 
            "--image", 
            help="ISO images",
            required=True
        )
        build.add_argument(
            "-p", 
            "--poc", 
            help="POC name",
            required=True
        )
        build.add_argument(
            "-a", 
            "--amount", 
            help="Amout of vms to create",
            required=True
        )

        args = parser.parse_args()



ArgsParser()
