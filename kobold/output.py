from .taskdb import TaskDB
from .task import Task

from typing import List
from copy import copy
from rich.text import Text


class ListPrinter:
    def __init__(self, tdb: TaskDB, hide_done: bool = True, project: str = None):
        self.tdb = tdb
        self.project = project
        self.hide_done = hide_done

    def filter_tasks(self) -> List[Task]:
        filtered = copy(self.tdb.tasks)
        if self.hide_done:
            filtered = {k: task for k, task in filtered.items() if not task.done}
        if self.project:
            filtered = {
                k: task for k, task in filtered.items() if self.project == task.project
            }
        filtered = {k: v for k, v in sorted(filtered.items(), key=lambda x: x[1].project)}
        return filtered

    def __call__(self) -> Text:
        tasks = [format_task(t, h) for h, t in self.filter_tasks().items()]
        return Text("\n").join(tasks)

    def __repr__(self):
        return str(self.tdb)


def format_task(t: Task, h: str) -> Text:
    if t.done:
        return Text(f"{h} {t}", style="bright_black")
    hash = Text(h, style="green")
    project = Text(f"{t.project}:", style="blue")
    name = Text(t.name)
    return Text(" ").join([hash, project, name])
