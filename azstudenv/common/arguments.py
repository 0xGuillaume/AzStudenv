"""."""
import argparse


class ArgsParser:
    """."""

    def __init__(self):

        parser = argparse.ArgumentParser()



        parser.add_argument(
            "-i", 
            "--image", 
            help="ISO images",
            required=True
        )
        parser.add_argument(
            "-p", 
            "--poc", 
            help="POC name",
            required=True
        )
        parser.add_argument(
            "-a", 
            "--amount", 
            help="Amout of vms to create",
            required=True
        )


        self.subparser = parser.add_subparsers(title="Applying", help="Commands", dest="apply")

        parser_build = self.subparser.add_parser(
                "build", 
                help="Build AzStuden configuration", 
                add_help=False, 
                parents=[parser]
        )

        parser_apply = self.subparser.add_parser(
                "apply", 
                help="Applying Terraform plan", 
                add_help=False, 
                parents=[parser]
        )

        parser_destroy = self.subparser.add_parser(
                "destroy", 
                help="Destroying Terraform plan", 
                add_help=False, 
                parents=[parser]
        )

        args = parser.parse_args()

        print(args)

ArgsParser()
