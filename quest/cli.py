import arrow
from typer import Typer, Option, Argument, Context
from . import output, Task, YamlDB, load_user_configuration
from .date_utils import parse_date

import quest.trello as trello
from importlib.metadata import version


quest = Typer(help="A commandline quest log.")
trello_app = Typer()
debug_app = Typer()

quest.add_typer(debug_app, name="debug", help="Debug commands.")
quest.add_typer(trello_app, name="trello", help="Trello functionality.")

config = load_user_configuration()


@trello_app.command("boards", help="List Trello boards.")
def trello_boards():
    trello.get_boards(config.trello)


@trello_app.command("cards", help="List Trello cards.")
def trello_cards():
    tdb = trello.tasks(config.trello)
    output.taskdb(tdb)


@debug_app.command("cal", help="Display a calendar of this month.")
def debug_print_calendar(period: str = Option("month")):
    with YamlDB(config.path, "r") as tdb:
        output.calendar(tdb, period)


@debug_app.command("xp", help="List all rewarded XP.")
def debug_app_print_xp():
    with YamlDB(config.path, "r") as tdb:
        output.all_xp(tdb)


@debug_app.command("config", help="Show location of default quest files.")
def debug_config_dump():
    output.config_dump(config)


@quest.command("edit", help="Edit properties of existing tasks.")
def debug_edit(
    hash: str,
    project: str = Option(None, "--project", "-p"),
    xp: int = Option(None, "--xp", "-x"),
    state: str = Option(None, "--state", "-s"),
    due: str = Option(None, "--due", "-d", callback=parse_date),
    completed: str = Option(None, "--completed"),
):
    with YamlDB(config.path, "w") as tdb:
        t = tdb[hash]
        t.xp = xp or t.xp
        t.due = due or t.due
        t.project = project or t.project
        t.state = state or t.state
        t.completed = completed or t.completed
    output.task(t, hash)


@quest.command("summary", help="Print daily summary.")
def summary():
    with YamlDB(config.path, "r") as tdb:
        output.summary(tdb)


@quest.command("done", help="Mark a task as done.")
def mark_task_done(hash: str):
    with YamlDB(config.path, "w") as tdb:
        task = tdb[hash]
        task.state = "done"
    output.reward(task)


@quest.command("rm", help="Remove a task from the database entirely.")
def remove_task(hash: str):
    with YamlDB(config.path, "w") as tdb:
        t, h = tdb.pop(hash)
        output.task(t, h)


@quest.command("ls", help="List all open tasks.")
def list_tasks(
    hide_done: bool = Option(True), project: str = Option(None, "--project", "-p")
):
    with YamlDB(config.path, "r") as tdb:
        output.taskdb(tdb, project=project, hide_done=hide_done)


@quest.command("new", help="Create a new task.")
def add_task(
    entry: str,
    project: str = Option("void", "--project", "-p"),
    xp: int = Option(1, "--xp", "-x"),
    due: str = Option(None, "--due", "-d", callback=parse_date),
    state: str = Option("todo", "--state", "-s", callback=parse_date),
):
    task = Task(name=entry, project=project, xp=xp, due=due, state=state)
    with YamlDB(config.path, "w") as tdb:
        t, h = tdb.add(task)
        output.task(t, h)


@quest.command("version", help="Print version number.")
def get_version():
    print(version("quest"))


@quest.command("kanban", help="Print tasks as kanban board.")
def print_kanban(
    week: bool = Option(True, "--week", "-w"),
    today: bool = Option(False, "--today", "-t"),
):
    with YamlDB(config.path, "r") as tdb:
        output.kanban(tdb, week=week, today=today)


@quest.callback(invoke_without_command=True)
def callback(ctx: Context):
    if ctx.invoked_subcommand is None:
        summary()


def run():
    quest()
