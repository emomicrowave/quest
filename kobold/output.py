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
style_future = "yellow"
style_past = "magenta"
style_xp = "yellow"
style_bar = {"bg": "bright_black", "complete": "yellow", "finished": "green"}


def task_date(t: Task) -> Text:
    if t.state == "done":
        date = arrow.get(t.completed)
        style = style_past
    elif t.due:
        date = arrow.get(t.due)
        style = style_future
    else:
        return Text("")
    now = arrow.now()
    if date.hour == 0 and date.minute == 0:
        date = date.ceil("day")
        now = date.ceil("day")
    if date.isocalendar()[1] == now.isocalendar()[1]:
        date = date.humanize(granularity=["day"]) + " (" + date.format("ddd") + ")"
    else:
        date = date.humanize(granularity=["day"])
    # prettier
    if "in a day" in date:
        date = "tomorrow"
    elif "a day ago" in date:
        date = "yesterday"
    elif "0 days" in date:
        date = "today"
    date = Text(f"{date}", style=style)
    return date


def format_task(t: Task, h: str) -> Text:
    if not isinstance(t, Task):
        return Text("")
    hash = Text(h, style=style_hash.get(t.state, style_default))
    project = Text(f"{t.project}:", style=style_project)
    name = Text(t.name)
    date = task_date(t)
    task = Text(" ").join([p for p in [hash, project, name, date] if len(p) > 0])
    return task


def format_tdb(tdb: TaskDB) -> Text:
    return Text("\n").join([format_task(t, h) for h, t in tdb])


def taskdb(tdb: TaskDB):
    print(format_tdb(tdb))


def task(task: Task, hash: str):
    print(format_task(task, hash))


def summary(tdb: TaskDB):
    daily_xp(tdb)
    agenda(tdb)


def all_xp(tdb: TaskDB):
    text = Text(f"{tdb.xp}", style=style_xp)
    print(text)


def reward(task: Task):
    em = ":shooting_star:"
    reward = Text(f"{task.xp}", style=style_xp)
    print(format_task(task, ""), reward, em)


def agenda(tdb: TaskDB):
    predicate = lambda t: filters.todo(t) and filters.due_this_week(t)
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
    progress = Text(f" {xp}/{total}", style=style_xp)
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
    zipped = zip_longest(todo, in_progress, done, fillvalue="__")
    for tasks in zipped:
        formatted = [format_task(t, h) for h, t in tasks]
        table.add_row(*formatted)
    print(table)
