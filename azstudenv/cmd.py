import subprocess
import typer
import time
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import inspect


cmd1 = ["terraform", "-chdir=terraform/", "apply", "--auto-approve"],#, "-no-color"],
cmd2 = ["ls"]



def run(cmd:str):

    count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:

        with subprocess.Popen(
            ["terraform", cmd, "-auto-approve", "-no-color"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
        ) as process:
            progress.add_task(description="Creating AzStudenv infrastructure...", total=None)


            for line in process.stdout:
                line = line.decode("utf-8")

                if not line and not count:
                    message = "Terraform error while executing. Refer to the error message above."
                    #Console.error("*.tf", message)
                    return

                if not line and count:
                    break

                if "complete after" in line:
                    progress.update(
                        task_id=0,
                        description="Resource group created.", 
                        total=None
                    )
                    print(line)
                    count += 1


run("apply")
run("destroy")
