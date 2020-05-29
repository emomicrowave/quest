from .taskdb import TaskDB
from .task import Task
from . import filters

import arrow
from rich import print, box
from rich.text import Text
from rich.bar import Bar
from rich.table import Table
from functools import singledispatch
from itertools import zip_longest

style_default = "white"
style_hash = {"todo": "green", "in_progress": "yellow", "done": "bright_black"}
style_project = "blue"
style_done = "bright_black"
style_date = "yellow"
style_xp = "yellow"
style_bar = {"bg": "bright_black", "complete": "yellow", "finished": "green"}


@singledispatch
def format(arg, *args) -> Text:
    return ""


@format.register
def _(t: Task, h: str) -> Text:
    # if t.done:
    # return Text(f"{h} {t}", style=style_done)
    hash = Text(h, style=style_hash.get(t.state, style_default))
    project = Text(f"{t.project}:", style=style_project)
    name = Text(t.name)
    if t.due:
        due = arrow.get(t.due)
        now = arrow.now()
        if due.hour == 0 and due.minute == 0:
            due = due.ceil("day")
        if due.isocalendar()[1] == now.isocalendar()[1]:
            due = due.humanize(granularity=["day"]) + " (" + due.format("ddd") + ")"
        else:
            due = due.humanize(granularity=["day"])
        due = Text(f"{due}", style=style_date)
    else:
        due = ""
    return Text(" ").join([hash, project, name, due])


@format.register
def _(tdb: TaskDB) -> Text:
    return Text("\n").join([format(t, h) for h, t in tdb])


def taskdb(tdb: TaskDB):
    print(format(tdb))


def task(task: Task, hash: str):
    print(format(task, hash))


def summary(tdb: TaskDB):
    daily_xp(tdb)
    agenda(tdb)


def all_xp(tdb: TaskDB):
    text = Text(f"{tdb.xp}", style=style_xp)
    print(text)


def reward(task: Task):
    em = ":shooting_star:"
    reward = Text(f"{task.xp}", style=style_xp)
    print(format(task, ""), reward, em)


def agenda(tdb: TaskDB):
    predicate = lambda t: filters.todo(t) and filters.due_this_week(t)
    print(format(tdb.filter(predicate)))


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
    progress = Text(f" {xp}/{total}", style=style_xp)
    print(bar, progress)


def kanban(tdb: TaskDB, week=False, today=False):
    due_p = lambda t: (
        (not week or filters.due_this_week(t)) and (not today or filters.due_today(t))
    )
    completed_p = lambda t: (
        (not week or filters.completed_this_week(t)) and (not today or filters.completed_today(t))
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
    zipped = zip_longest(todo, in_progress, done, fillvalue="__")
    for tasks in zipped:
        formatted = [format(t, h) for h, t in tasks]
        table.add_row(*formatted)
    print(table)
