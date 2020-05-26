#!/home/hgf/.miniconda/envs/ork/bin/python
import yaml
from subprocess import run
from os import getenv
from typing import List
from pathlib import Path
from rich import print
from typer import Typer, Option, Argument, Context
from kobold.task import Task
from kobold.taskdb import TaskDB
from kobold.output import ListPrinter, format_task

app = Typer(add_completion=False)
config = {"path": Path.home().joinpath("cloud/kobold.yaml"), "tdb": None}


@app.command("done")
def mark_task_done(hash: str):
    config["tdb"].tasks[hash].complete()
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())
    em = ":glowing_star:"
    print(f"{em} Task complete! {em}")


@app.command("edit")
def edit_tasks_in_editor():
    run([getenv("EDITOR", "vi"), config["path"]])


@app.command("rm")
def remove_task(hash: str):
    config["tdb"].tasks.pop(hash)
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())


@app.command("ls")
def list_tasks(
    hide_done: bool = Option(True), project: str = Option(None, "--project", "-p")
):
    print(ListPrinter(config["tdb"], hide_done=hide_done, project=project)())


@app.command("new")
def add_task(
    entry: str,
    project: str = Option("void", "--project", "-p"),
    due: str = Option(None, "--due", "-d"),
):
    task = Task(name=entry, project=project, due=due)
    t, h = config["tdb"].add_task(task)
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())
    print(format_task(t, h))


@app.command("track")
def track_task(hash: str, comment: str = Option("", "--comment", "-c")):
    task = config["tdb"].tasks[hash]
    entry = f"🥕 {task.project}: {task.name} {comment}".strip()
    with open(Path.home().joinpath(".current_task"), "w") as f:
        f.write(entry)


@app.callback(invoke_without_command=True)
def callback(ctx: Context):
    global config

    with open(config["path"]) as f:
        tasks = yaml.load(f, Loader=yaml.Loader)
    config["tdb"] = TaskDB(tasks)

    if ctx.invoked_subcommand is None:
        list_tasks(True, None)


if __name__ == "__main__":
    app()
