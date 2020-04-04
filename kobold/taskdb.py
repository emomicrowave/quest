from .task import Task, PrettyTask
from .tag import parse_tag
from typing import List


class TaskDB:
    def __init__(self, filename: str = None):
        self.tasks = {}
        if filename:
            self.filename = filename
            self.load_tasks()

    def load_tasks(self):
        with open(self.filename, "r") as f:
            for entry in f.readlines():
                self.add_task(entry)

    def save_tasks(self):
        sorted_tasks = sorted(
            self.tasks.values(), key=lambda x: x.hash + 0x10000 if x.done else 0
        )
        all_tasks = "\n".join([str(t) for t in sorted_tasks])
        with open(self.filename, "w") as f:
            f.write(all_tasks)

    def add_task(self, entry: str):
        salt = 0
        while (t := Task(entry, str(salt).encode())).hash in self.tasks.keys():
            salt += 1
        self.tasks[t.hash] = t
        return t

    def remove_task(self, hash: int):
        self.tasks.pop(hash)

    def __repr__(self):
        return "\n".join([str(t) for t in self.tasks.values()])


class PrettyTaskDB(TaskDB):
    def __init__(self, tdb: TaskDB, hide_done: bool = True, filters: List[str] = None):
        self.tasks = {hash: PrettyTask(task) for hash, task in tdb.tasks.items()}
        self.hide_done = hide_done
        self.filename = tdb.filename
        self.filters = [parse_tag(t) for t in filters] if filters else []

    def filter(self, tasks: List[Task]):
        pred_done = lambda t: not (self.hide_done and t.done)
        pred_tags = lambda t: all([tag in t.tags for tag in self.filters])
        pred = lambda t: pred_done(t) and pred_tags(t)
        return [t for t in tasks if pred(t)]

    def __repr__(self):
        return "\n".join([str(t) for t in self.filter(self.tasks.values())])
