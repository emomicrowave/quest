from .taskdb import TaskDB
from .task import Task

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
    return Text(" ").join([hash, project, name])

@format.register
def _(tdb: TaskDB) -> Text:
    tasks = {h: t for h, t in sorted(tdb.tasks.items(), key=lambda x: x[1].project)}
    return Text("\n").join([format(t, h) for h, t in tasks.items()])

