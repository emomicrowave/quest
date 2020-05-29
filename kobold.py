#!/home/hgf/.miniconda/envs/ork/bin/python
from subprocess import run
from os import getenv
from pathlib import Path
from typer import Typer, Option, Argument, Context
from kobold import output, Task, YamlDB

kobold = Typer()
debug = Typer(add_completion=False)
kobold.add_typer(debug, name="debug")

config = {"path": Path.home() / "cloud/kobold.yaml"}


@debug.command("xp")
def debug_print_xp():
    with YamlDB(config["path"], "r") as tdb:
        output.all_xp(tdb)


@debug.command("start")
def debug_start_task(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        task = tdb.tasks[hash]
        task.state = "in_progress"


@debug.command("agenda")
def debug_agenda():
    with YamlDB(config["path"], "r") as tdb:
        output.agenda(tdb)


@kobold.command("summary")
def summary():
    with YamlDB(config["path"], "r") as tdb:
        output.summary(tdb)


@kobold.command("done")
def mark_task_done(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        task = tdb.tasks[hash]
        task.state = "done"
    output.reward(task)


@kobold.command("edit")
def edit_tasks_in_editor():
    cmd = getenv("VISUAL", "vi").split()
    run(cmd + [config["path"]])


@kobold.command("rm")
def remove_task(hash: str):
    with YamlDB(config["path"], "w") as tdb:
        t, h = tdb.pop(hash)
        output.task(t, h)


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
        output.taskdb(tdb.filter(lambda t: all([f(t) for f in filters])))


@kobold.command("new")
def add_task(
    entry: str,
    project: str = Option("void", "--project", "-p"),
    context: str = Option(None, "--context", "-c"),
    xp: float = Option(1, "--xp", "-x"),
    due: str = Option(None, "--due", "-d"),
):
    task = Task(name=entry, project=project, context=context, xp=xp, due=due)
    with YamlDB(config["path"], "w") as tdb:
        t, h = tdb.add(task)
        output.task(t, h)


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
        summary()


if __name__ == "__main__":
    kobold()
