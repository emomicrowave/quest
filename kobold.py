#!/home/hgf/.miniconda/envs/ork/bin/python
import hashlib
from subprocess import run
import os
import sys
import git
import yaml
from typing import List
from pathlib import Path
from rich import print
from typer import Typer, Option, Argument, Context
from kobold.task import Task
from kobold.taskdb import TaskDB
from kobold.output import ListPrinter

app = Typer()
config = {"path": Path.home().joinpath("cloud/kobold.yaml"), "tdb": None}


@app.command("done")
def mark_task_done(hash: str):
    config["tdb"].tasks[hash].complete()
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())


@app.command("edit")
def edit_tasks_in_editor():
    run([os.getenv("EDITOR", "vi"), config["path"]])


@app.command("rm")
def remove_task(hash: str):
    config["tdb"].tasks.pop(hash)
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())


@app.command("ls")
def list_tasks(
    hide_done: bool = Option(True),
    project: str = Option(None, "--project", "-p"),
):
    print(ListPrinter(config["tdb"], hide_done=hide_done, project=project)())


@app.command("new")
def add_task(entry: List[str]):
    config["tdb"].add_task(" ".join(entry))
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())


@app.callback(invoke_without_command=True)
def callback(ctx: Context):
    global config

    with open(config["path"]) as f:
        tasks = yaml.load(f, Loader=yaml.Loader)
    config["tdb"] = TaskDB(tasks)

    if ctx.invoked_subcommand is None:
        list_tasks(filters=None)


if __name__ == "__main__":
    app()
