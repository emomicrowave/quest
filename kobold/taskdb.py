from .task import Task
import parse
import hashlib
import yaml
from typing import Dict


class TaskDB:
    def __init__(self, tasks: Dict[str, str]):
        self.tasks = {k: Task(v) for k, v in tasks.items()}

    def add_task(self, entry: str):
        salt = 0
        while (h := self._hash(entry, salt)) in self.tasks.keys():
            salt += 1
        t = Task(entry)
        self.tasks[h] = t
        return t, h

    def _hash(self, entry: str, salt: int) -> str:
        salt = str(salt).encode()
        hash = int(
            hashlib.blake2b(entry.encode(), digest_size=2, salt=salt).hexdigest(),
            base=16,
        )
        format_hash = lambda h: f"{hex(h).lstrip('0x').zfill(4)}"
        return format_hash(hash)

    def remove_task(self, hash: str):
        self.tasks.pop(hash)

    def dump(self):
        return yaml.dump({k: v.entry for k, v in self.tasks.items()})

    def __repr__(self):
        sorted_tasks = sorted(
            self.tasks.items(), key=lambda task: task[0] + (0x10000 if task[1].done else 0)
        )
        all_tasks = "\n".join([f"{x[0]} {x[1]}" for x in sorted_tasks])
        return all_tasks
