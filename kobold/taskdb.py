from .task import Task
import parse
import hashlib
import yaml
from typing import Dict


class TaskDB:
    def __init__(self, tasks: Dict[str, str]):
        self.tasks = {k: Task(**v) for k, v in tasks.items()}

    def add_task(self, task: Task):
        salt = 0
        while (hash := self._hash(str(task), salt)) in self.tasks.keys():
            salt += 1
        self.tasks[hash] = task
        return task, hash

    def pop(self, hash: str):
        return self.tasks.pop(hash), hash

    def filter(self, *preds):
        for pred in preds:
            self.tasks = {k: t for k, t in self.tasks.items() if pred(t)}
        return self

    def dump(self):
        return yaml.dump({h: t.to_dict() for h, t in self.tasks.items()})

    def _hash(self, entry: str, salt: int) -> str:
        salt = str(salt).encode()
        hash = int(
            hashlib.blake2b(entry.encode(), digest_size=2, salt=salt).hexdigest(),
            base=16,
        )
        format_hash = lambda h: f"{hex(h).lstrip('0x').zfill(4)}"
        return format_hash(hash)

    def __repr__(self):
        all_tasks = "\n".join([f"{h}: {t}" for h, t in self.tasks.items()])
        return all_tasks

class YamlDB:
    def __init__(self, filename: str, mode: str = "r"):
        assert mode in "rw"
        self.filename = filename
        self.mode = mode

    def __enter__(self) -> TaskDB:
        with open(self.filename, "r") as f:
            tasks = yaml.load(f, Loader=yaml.Loader)
        self.taskdb = TaskDB(tasks)
        return self.taskdb

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.mode == "w":
            with open(self.filename, "w") as f:
                f.writelines(self.taskdb.dump())

