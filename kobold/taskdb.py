from .task import Task
import parse
import hashlib
import yaml
import arrow
from typing import Union, Dict
from pathlib import Path


class TaskDB:
    def __init__(self, tasks: Union[Dict[str, str], Dict[str, Task]]):
        tasks = tasks or {}
        self.tasks = {k: (v if isinstance(v, Task) else Task(**v)) for k, v in tasks.items()}

    def add(self, task: Task):
        salt = 0
        while (hash := self._hash(str(task), salt)) in self.tasks.keys():
            salt += 1
        self.tasks[hash] = task
        return task, hash

    def pop(self, hash: str):
        return self.tasks.pop(hash), hash

    def filter(self, preds):
        pred = lambda t: all([p(t) for p in preds])
        tasks = {k: t for k, t in self.tasks.items() if pred(t)}
        return TaskDB(tasks)

    def _hash(self, entry: str, salt: int) -> str:
        salt = str(salt).encode()
        hash = int(
            hashlib.blake2b(entry.encode(), digest_size=2, salt=salt).hexdigest(),
            base=16,
        )
        hash = hex(hash).lstrip('0x').zfill(4)
        return hash

    def __repr__(self):
        all_tasks = "\n".join([f"{h}: {t}" for h, t in self.tasks.items()])
        return all_tasks

class YamlDB:
    def __init__(self, filename: str, mode: str = "r"):
        assert mode in "rw"
        self.filename = filename
        self.mode = mode

    def backup(self, content):
        backup_name = Path.home() / ".local/share/kobold" / f"kobold_backup_{arrow.now().format('YYYY-MM-DDTHH-mm-ss')}"
        with open(backup_name, "w") as f:
            f.write(content)

    def __enter__(self) -> TaskDB:
        with open(self.filename, "r") as f:
            tasks = yaml.load(f, Loader=yaml.Loader)
            f.seek(0)
            content = f.read()
        if self.mode == "w":
            self.backup(content)
        self.taskdb = TaskDB(tasks)
        return self.taskdb

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.mode == "w":
            with open(self.filename, "w") as f:
                as_yaml = yaml.dump({h: t.to_dict() for h, t in self.taskdb.tasks.items()})
                f.writelines(as_yaml)

