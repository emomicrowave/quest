from .taskdb import TaskDB
from .task import Task
from .tag import parse_tag

from typing import List
from rich.text import Text

class ListPrinter:
    def __init__(self, tdb: TaskDB, hide_done: bool = True, filters: List[str] = None):
        self.tdb = tdb
        self.hide_done = hide_done
        self.filters = [parse_tag(t) for t in filters] if filters else []

    def pred(self, task: Task):
        pred_done = lambda t: not (self.hide_done and t.done)
        pred_tags = lambda t: all([tag in t.tags for tag in self.filters])
        pred = lambda t: pred_done(t) and pred_tags(t)
        return pred(task)

    def format_task(self, t: Task, h: int):
        h = hex(h).lstrip('0x').zfill(4)
        if t.done:
            return Text(f"{h} {t.entry}", style="bright_black")
        tags = [Text(h, style="green")]
        for tag in t.iterwords():
            if tag.type == "project":
                style = "magenta"
            elif tag.type == "context":
                style = "cyan"
            elif tag.type == "word":
                style = None
            else:
                style = "blue"
            tags.append(Text(str(tag), style=style))
        return Text(" ").join(tags)

    def filter_tasks(self) -> List[Task]:
        filtered_tasks = {h: t for h, t in self.tdb.tasks.items() if self.pred(t)}
        return filtered_tasks


    def __call__(self):
        return Text("\n").join([self.format_task(t, h) for h, t in self.filter_tasks().items()])

    def __repr__(self):
        filtered_tasks = {h: t for h, t in self.tdb.tasks.items() if self.pred(t)}
        filtered_tdb = TaskDB()
        filtered_tdb.tasks = filtered_tasks
        return str(filtered_tdb)
