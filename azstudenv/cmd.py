import subprocess
import typer
import time
from rich.progress import Progress
from rich import inspect


cmd1 = ["terraform", "-chdir=terraform/", "apply", "--auto-approve"],#, "-no-color"],
cmd2 = ["ls"]



def run(cmd:str):

    count = 0

    with Progress() as progress:

        step = progress.add_task(f"[green]{cmd.capitalize()}ing...", total=1)

        with subprocess.Popen(
            ["terraform", cmd, "-auto-approve", "-no-color"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
        ) as process:

            for line in process.stdout:
                line = line.decode("utf-8")

                if not line and not count:
                    message = "Terraform error while executing. Refer to the error message above."
                    #Console.error("*.tf", message)
                    return

                if not line and count:
                    break

                if "complete after" in line:
                    progress.update(step, advance=1)
                    print(line)
                    count += 1


run("apply")
run("destroy")
