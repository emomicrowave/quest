from .taskdb import TaskDB
from .task import Task

import arrow
from rich import print
from rich.text import Text
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
        due = Text("")
    return Text(" ").join([hash, project, name, due])

@format.register
def _(tdb: TaskDB) -> Text:
    due, rest = {}, {}
    for h, t in tdb.tasks.items():
        (due if t.due else rest)[h] = t
    due = [format(t, h) for h, t in sorted(due.items(), key=lambda x: x[1].due)]
    rest  = [format(t, h) for h, t in sorted(rest.items(), key=lambda x: x[1].project)]
    return Text("\n").join(due + rest)

def print_taskdb(tdb: TaskDB):
    print(format(tdb))

def print_task(task: Task, hash: str):
    print(format(task, hash))

def print_summary(tdb: TaskDB):
    daily_xp = sum(
        [
            t.xp
            for t in tdb.tasks.values()
            if t.done and arrow.get(t.completed).date() == arrow.now().date()
        ]
    )
    reward = Text(f"{daily_xp}xp", style="bold yellow")
    print("Daily:", reward)

def print_all_xp(tdb: TaskDB):
    total_xp = sum([t.xp for t in tdb.tasks.values() if t.done])
    text = Text(f"{total_xp}xp", style="yellow")
    print(text)

def print_reward(task: Task):
    em = ":glowing_star:"
    reward = Text(f"{task.xp}xp", style="bold yellow")
    print(em, reward, em)

def print_agenda(tdb: TaskDB):
    is_today = lambda t: t.due is not None and arrow.get(t.due).isocalendar()[:2] == arrow.now().isocalendar()[:2]
    is_todo = lambda t: t.state == "todo"
    print(format(tdb.filter([is_today, is_todo])))

