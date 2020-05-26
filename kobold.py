#!/home/hgf/.miniconda/envs/ork/bin/python
import arrow
from subprocess import run
from os import getenv
from typing import List
from pathlib import Path
from rich import print
from rich.text import Text
from typer import Typer, Option, Argument, Context
from kobold.task import Task
from kobold.taskdb import YamlDB
from kobold.output import format

kobold = Typer(add_completion=False)
debug = Typer(add_completion=False)
kobold.add_typer(debug, name="debug")

config = {"path": Path.home().joinpath("cloud/kobold.yaml")}


@debug.command("xp")
def debug_print_xp():
    with YamlDB(config["path"], "r") as tdb:
        total_xp = sum([t.xp for t in tdb.tasks.values() if t.done])
    text = Text(f"{total_xp}xp", style="yellow")
    print(text)


@debug.command("daily_xp")
def debug_print_daily_xp():
    with YamlDB(config["path"], "r") as tdb:
        daily_xp = sum(
            [
                t.xp
                for t in tdb.tasks.values()
                if t.done and arrow.get(t.completed).date() == arrow.now().date()
            ]
        )
    text = Text(f"{daily_xp}xp", style="yellow")
    print(text)


@kobold.command("done")
def mark_task_done(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        t = tdb.tasks[hash].complete()
    em = ":glowing_star:"
    print(f"{em} [yellow]{t.xp}xp {em}")


@kobold.command("edit")
def edit_tasks_in_editor():
    cmd = getenv("VISUAL", "vi").split()
    run(cmd + [config["path"]])


@kobold.command("rm")
def remove_task(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        t, h = tdb.pop(hash)
    print(format(t, h))


@kobold.command("ls")
def list_tasks(
    hide_done: bool = Option(True), project: str = Option(None, "--project", "-p")
):
    with YamlDB(config["path"], "r") as tdb:
        print(format(tdb.filter(lambda t: not t.done)))


@kobold.command("new")
def add_task(
    entry: str,
    project: str = Option("void", "--project", "-p"),
    context: str = Option(None, "--context", "-c"),
    xp: int = Option(1, "--xp", "-x"),
    due: str = Option(None, "--due", "-d"),
):
    task = Task(name=entry, project=project, context=context, xp=xp, due=due)
    with YamlDB(config["path"], "w") as tdb:
        t, h = tdb.add_task(task)
    print(format(t, h))


@kobold.command("track")
def track_task(hash: str, comment: str = Option("", "--comment", "-c")):
    with YamlDB(config["path"], "r") as tdb:
        task = tdb.tasks[hash]
    entry = f"🥕 {task.project}: {task.name} {comment}".strip()
    with open(Path.home().joinpath(".current_task"), "w") as f:
        f.write(entry)


@kobold.callback(invoke_without_command=True)
def callback(ctx: Context):
    if ctx.invoked_subcommand is None:
        list_tasks(True, None)


if __name__ == "__main__":
    kobold()
