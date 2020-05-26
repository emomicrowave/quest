#!/home/hgf/.miniconda/envs/ork/bin/python
import yaml
import arrow
from subprocess import run
from os import getenv
from typing import List
from pathlib import Path
from rich import print
from rich.text import Text
from typer import Typer, Option, Argument, Context
from kobold.task import Task
from kobold.taskdb import TaskDB
from kobold.output import ListPrinter, format_task

app = Typer(add_completion=False)
debug = Typer(add_completion=False)
app.add_typer(debug, name="debug")

config = {"path": Path.home().joinpath("cloud/kobold.yaml"), "tdb": None}


@debug.command("xp")
def debug_print_xp():
    total_xp = sum([t.xp for t in config["tdb"].tasks.values() if t.done])
    text = Text(f"{total_xp}xp", style="yellow")
    print(text)


@debug.command("daily_xp")
def debug_print_daily_xp():
    daily_xp = sum(
        [
            t.xp
            for t in config["tdb"].tasks.values()
            if t.done and arrow.get(t.completed).date() == arrow.now().date()
        ]
    )
    print(f"[yellow]{daily_xp}xp")


@app.command("done")
def mark_task_done(hash: str):
    t = config["tdb"].tasks[hash].complete()
    with open(config["path"], "w") as f:
        f.writelines(config["tdb"].dump())
    em = ":glowing_star:"
    print(f"{em} [yellow]{t.xp}xp {em}")


@app.command("edit")
def edit_tasks_in_editor():
    cmd = getenv("VISUAL", "vi").split()
    run(cmd + [config["path"]])


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
    context: str = Option(None, "--context", "-c"),
    xp: int = Option(1, "--xp", "-x"),
    due: str = Option(None, "--due", "-d"),
):
    task = Task(name=entry, project=project, context=context, xp=xp, due=due)
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
