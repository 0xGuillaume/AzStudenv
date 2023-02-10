from typing import Literal
import subprocess
import typer
import time
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import inspect


cmd1 = ["terraform", "-chdir=terraform/", "apply", "--auto-approve"],#, "-no-color"],
cmd2 = ["ls"]


def cmd(option: Literal["apply", "destroy"]) -> None:
    """
    """

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:

        with subprocess.Popen(
            ["terraform", option, "-auto-approve", "-no-color"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
        ) as process:
            task = progress.add_task(
                description=f"{option.capitalize()}ing AzStudenv infrastructure...", 
                total=None
            )

            for line in process.stdout:
                line = line.decode("utf-8")

                if "complete after" in line:
                    print(line)

