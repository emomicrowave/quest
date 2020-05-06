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

    def format_task(self, t: Task, h: str) -> Text:
        if t.done:
            return Text(f"{h} {t}", style="bright_black")
        task = Text(f"{h} {t}")
        task.highlight_regex(r"^[0-9a-f]{4}", "green")
        task.highlight_regex(r"\+\w+", "blue")
        return task

    def filter_tasks(self) -> List[Task]:
        filtered = copy(self.tdb.tasks)
        if self.hide_done:
            filtered = {k: v for k, v in filtered.items() if not v.done}
        if self.project:
            filtered = {k: v for k, v in filtered.items() if self.project == v.project}
        return filtered

    def __call__(self) -> Text:
        return Text("\n").join([self.format_task(t, h) for h, t in self.filter_tasks().items()])

    def __repr__(self):
        return str(self.tdb)
