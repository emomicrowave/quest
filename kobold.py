#!/home/hgf/.miniconda/envs/ork/bin/python
from subprocess import run
from os import getenv
from pathlib import Path
from typer import Typer, Option, Argument, Context
from kobold.task import Task
from kobold.taskdb import YamlDB
from kobold.output import (
    print_task,
    print_taskdb,
    print_summary,
    print_all_xp,
    print_reward,
    print_agenda,
)

kobold = Typer()
debug = Typer(add_completion=False)
kobold.add_typer(debug, name="debug")

config = {"path": Path.home() / "cloud/kobold.yaml"}


@debug.command("xp")
def debug_print_xp():
    with YamlDB(config["path"], "r") as tdb:
        print_all_xp(tdb)


@debug.command("agenda")
def debug_agenda():
    with YamlDB(config["path"], "r") as tdb:
        print_agenda(tdb)



@kobold.command("summary")
def summary():
    with YamlDB(config["path"], "r") as tdb:
        print_summary(tdb)


@kobold.command("done")
def mark_task_done(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        task = tdb.tasks[hash].complete()
        print_reward(task)


@kobold.command("edit")
def edit_tasks_in_editor():
    cmd = getenv("VISUAL", "vi").split()
    run(cmd + [config["path"]])


@kobold.command("rm")
def remove_task(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        t, h = tdb.pop(hash)
        print_task(t, h)


@kobold.command("ls")
def list_tasks(
    hide_done: bool = Option(True), project: str = Option(None, "--project", "-p")
):
    filters = []
    if hide_done:
        filters.append(lambda t: not t.done)
    if project:
        filters.append(lambda t: t.project == project)
    with YamlDB(config["path"], "r") as tdb:
        print_taskdb(tdb.filter(filters))


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
        t, h = tdb.add(task)
        print_task(t, h)


@kobold.command("track")
def track_task(hash: str, comment: str = Option("", "--comment", "-c")):
    with YamlDB(config["path"], "r") as tdb:
        task = tdb.tasks[hash]
    entry = f"🥕 {task.project}: {task.name} {comment}".strip()
    with open(Path.home() / ".current_task", "w") as f:
        f.write(entry)


@kobold.callback(invoke_without_command=True)
def callback(ctx: Context):
    if ctx.invoked_subcommand is None:
        list_tasks(True, None)


if __name__ == "__main__":
    kobold()
