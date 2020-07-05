from ..taskdb import TaskDB
from ..task import Task
from .. import filters
from ..date_utils import humanize
from ..configuration import Configuration

import arrow
from rich import print, box
from rich.text import Text
from rich.bar import Bar
from rich.table import Table, Column
from functools import singledispatch
from itertools import zip_longest

style_default = "white"
style_hash = {"todo": "green", "in_progress": "yellow", "done": "bright_black"}
style_project = {"done": "bright_black", "default": "blue"}
style_done = "bright_black"
style_early_bird = "green"
style_due = "yellow"
style_overdue = "bright_red"
style_completed = "magenta"
style_xp = "yellow"
style_bar = {"bg": "bright_black", "complete": "yellow", "finished": "green"}


def task_date(t: Task) -> Text:
    if t.state == "done":
        date = humanize(t.completed)
        style = style_completed
    elif t.due:
        date = humanize(t.due)
        if filters.overdue(t):
            style = style_overdue
        elif filters.due_remaining(t, 2):
            style = style_early_bird
        else:
            style = style_due
    else:
        date = ""
        style = ""

    return Text(date, style=style)


def format_task(t: Task, h: str, with_hash=True, with_date=True) -> Text:
    hash = Text(h, style=style_hash.get(t.state, style_default))
    project = Text(
        f"{t.project}:", style=style_project.get(t.state, style_project["default"])
    )
    name = Text(t.name)
    date = task_date(t)

    parts = [
        hash if with_hash else None,
        project if t.project else None,
        name,
        date if with_date else None,
    ]
    task = Text(" ", end="").join([p for p in parts if p is not None])
    return task


def format_tdb(tdb: TaskDB, with_hash=True, with_date=True) -> Text:
    return Text("\n").join([format_task(t, h, with_hash, with_date) for h, t in tdb])


def taskdb(tdb: TaskDB, project: str = None, hide_done=True):
    if hide_done:
        tdb = tdb.filter(filters.todo)
    if project:
        tdb = tdb.filter(lambda t: t.project == project)
    print(format_tdb(tdb))


def task(task: Task, hash: str):
    print(format_task(task, hash), "\n")


def summary(tdb: TaskDB):
    daily_xp(tdb)
    agenda(tdb)


def all_xp(tdb: TaskDB):
    text = Text(f"{tdb.xp}", style=style_xp)
    print(text)


def reward(task: Task):
    reward = Text(f" {task.xp} xp", style=style_xp)
    print(format_task(task, ""), reward)


def agenda(tdb: TaskDB):
    predicate = lambda t: filters.todo(t) and (
        filters.due_this_week(t) or filters.overdue(t)
    )
    print(format_tdb(tdb.filter(predicate)))


def daily_xp(tdb: TaskDB):
    total = 10
    completed = tdb.filter(filters.completed_today)
    xp = completed.xp
    bar = Bar(
        total=total,
        completed=xp,
        width=30,
        style=style_bar.get("bg", style_default),
        complete_style=style_bar.get("complete", style_default),
        finished_style=style_bar.get("finished", style_default),
    )
    progress = Text(
        f" {xp}/{total}",
        style=style_bar.get("complete") if xp < total else style_bar.get("finished"),
    )
    print(bar, progress)


def kanban(tdb: TaskDB, week=False, today=False):
    due_p = lambda t: (
        (not week or filters.due_this_week(t)) and (not today or filters.due_today(t))
    )
    completed_p = lambda t: (
        (not week or filters.completed_this_week(t))
        and (not today or filters.completed_today(t))
    )
    todo = tdb.filter(lambda t: due_p(t) and t.state == "todo")
    in_progress = tdb.filter(lambda t: due_p(t) and t.state == "in_progress")
    done = tdb.filter(completed_p)
    table = Table(
        f"todo [yellow]{todo.xp}",
        f"in progress [yellow]{in_progress.xp}",
        f"done [yellow]{done.xp}",
        box=box.ROUNDED,
    )
    zipped = zip_longest(todo, in_progress, done, fillvalue=("", Task()))
    for tasks in zipped:
        formatted = [format_task(t, h) for h, t in tasks]
        table.add_row(*formatted)
    print(table)


def config_dump(config: Configuration):
    print(config)
