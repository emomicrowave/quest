#!/home/hgf/.miniconda/envs/ork/bin/python
from typer import Typer, Option, Argument, Context
from kobold import output, Task, YamlDB, filters, load_user_configuration
import kobold.trello as trello


kobold = Typer()
debug_app = Typer(name="kobold", add_completion=False)
trello_app = Typer()
kobold.add_typer(debug_app, name="debug")
kobold.add_typer(trello_app, name="trello")

config = load_user_configuration()


@trello_app.command("boards")
def trello_boards():
    trello.get_boards()


@trello_app.command("cards")
def trello_cards():
    trello.get_cards()


@debug_app.command("xp")
def debug_app_print_xp():
    with YamlDB(config.path, "r") as tdb:
        output.all_xp(tdb)


@debug_app.command("config")
def debug_load_config():
    config = load_user_configuration()
    from IPython import embed

    embed()


@kobold.command("edit")
def debug_edit(
    hash: str,
    project: str = Option(None, "--project", "-p"),
    context: str = Option(None, "--context", "-c"),
    xp: int = Option(None, "--xp", "-x"),
    due: str = Option(None, "--due", "-d"),
    state: str = Option(None, "--state", "-s"),
    completed: str = Option(None, "--completed"),
):
    with YamlDB(config.path, "w") as tdb:
        t = tdb[hash]
        t.xp = xp or t.xp
        t.due = due or t.due
        t.project = project or t.project
        t.context = context or t.context
        t.state = state or t.state
        t.completed = completed or t.completed
        output.task(t, hash)


@kobold.command("summary")
def summary():
    with YamlDB(config.path, "r") as tdb:
        output.summary(tdb)


@kobold.command("done")
def mark_task_done(hash: str):
    with YamlDB(config.path, "w") as tdb:
        task = tdb[hash]
        task.state = "done"
    output.reward(task)


@kobold.command("rm")
def remove_task(hash: str):
    with YamlDB(config.path, "w") as tdb:
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
    with YamlDB(config.path, "r") as tdb:
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
    with YamlDB(config.path, "w") as tdb:
        t, h = tdb.add(task)
        output.task(t, h)


@kobold.command("track")
def track_task(hash: str, comment: str = Option("", "--comment", "-c")):
    with YamlDB(config.path, "r") as tdb:
        task = tdb[hash]
    entry = f"🥕 {task.project}: {task.name} {comment}".strip()
    with open(config.taskfile, "w") as f:
        f.write(entry)


@kobold.command("kanban")
def print_kanban(
    week: bool = Option(True, "--week", "-w"),
    today: bool = Option(False, "--today", "-t"),
):
    with YamlDB(config.path, "r") as tdb:
        output.kanban(tdb, week=week, today=today)


@kobold.callback(invoke_without_command=True)
def callback(ctx: Context):
    if ctx.invoked_subcommand is None:
        summary()


if __name__ == "__main__":
    kobold()
