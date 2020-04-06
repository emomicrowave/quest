from .taskdb import TaskDB
from .task import Task
from .tag import parse_tag

from typing import List

class ListPrinter:
    def __init__(self, tdb: TaskDB, hide_done: bool = True, filters: List[str] = None):
        self.tasks = tdb.tasks
        self.hide_done = hide_done
        self.filename = tdb.filename
        self.filters = [parse_tag(t) for t in filters] if filters else []
        self.tdb = tdb

    def pred(self, task: Task):
        pred_done = lambda t: not (self.hide_done and t.done)
        pred_tags = lambda t: all([tag in t.tags for tag in self.filters])
        pred = lambda t: pred_done(t) and pred_tags(t)
        return pred(task)

    def __repr__(self):
        filtered_tasks = {h: t for h, t in self.tasks.items() if self.pred(t)}
        format_hash = lambda h: f"{hex(h).lstrip('0x').zfill(4)}"
        return "\n".join([f"{format_hash(h)} {t}" for h, t in filtered_tasks.items()])
