from .taskdb import TaskDB
from .task import Task

from typing import List
from rich.text import Text

class ListPrinter:
    def __init__(self, tdb: TaskDB, hide_done: bool = True, filters: List[str] = None):
        self.tdb = tdb

    def format_task(self, t: Task, h: str) -> Text:
        if t.done:
            return Text(f"{h} {t}", style="bright_black")
        task = Text(f"{h} {t}")
        task.highlight_regex(r"^[0-9a-f]{4}", "green")
        task.highlight_regex(r"\+\w+", "blue")
        return task

    def filter_tasks(self) -> List[Task]:
        filtered = {k: v for k, v in self.tdb.tasks.items() if not v.done}
        return filtered

    def __call__(self) -> Text:
        return Text("\n").join([self.format_task(t, h) for h, t in self.filter_tasks().items()])

    def __repr__(self):
        return str(self.tdb)
