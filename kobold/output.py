from .taskdb import TaskDB
from .task import Task

import arrow
from rich import print
from rich.text import Text
from rich.bar import Bar
from functools import singledispatch


@singledispatch
def format(arg, *args) -> Text:
    return Text("Something went wrong!", style="red")

@format.register
def _(t: Task, h: str) -> Text:
    if t.done:
        return Text(f"{h} {t}", style="bright_black")
    hash = Text(h, style="green")
    project = Text(f"{t.project}:", style="blue")
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
        due = Text(f"{due}", style="yellow")
    else:
        due = ""
    return Text(" ").join([hash, project, name, due])

@format.register
def _(tdb: TaskDB) -> Text:
    due, rest = {}, {}
    for h, t in tdb.tasks.items():
        (due if t.due else rest)[h] = t
    due = [format(t, h) for h, t in sorted(due.items(), key=lambda x: x[1].due)]
    rest  = [format(t, h) for h, t in sorted(rest.items(), key=lambda x: x[1].project)]
    return Text("\n").join(due + rest)

def taskdb(tdb: TaskDB):
    print(format(tdb))

def task(task: Task, hash: str):
    print(format(task, hash))

def summary(tdb: TaskDB):
    daily_xp(tdb)
    agenda(tdb)

def all_xp(tdb: TaskDB):
    total_xp = sum([t.xp for t in tdb.tasks.values() if t.done])
    text = Text(f"{total_xp}xp", style="yellow")
    print(text)

def reward(task: Task):
    em = ":glowing_star:"
    reward = Text(f"{task.xp}xp", style="bold yellow")
    print(em, reward, em)

def agenda(tdb: TaskDB):
    is_this_week = lambda t: t.due is not None and arrow.get(t.due).isocalendar()[:2] == arrow.now().isocalendar()[:2]
    is_todo = lambda t: t.state == "todo"
    predicate = lambda t: all([p(t) for p in [is_todo, is_this_week]])
    print(format(tdb.filter(predicate)))

def daily_xp(tdb: TaskDB):
    total = 10
    daily = sum(
        [
            t.xp
            for t in tdb.tasks.values()
            if t.done and arrow.get(t.completed).date() == arrow.now().date()
        ]
    )
    bar = Bar(
            total=total,
            completed=daily,
            width=30,
            style="bright_black",
            complete_style="yellow",
            finished_style="green",
            )
    progress = Text(f" {daily}/{total}", style="yellow")
    print(bar, progress)
