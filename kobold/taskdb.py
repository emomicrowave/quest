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
        return yaml.dump({h: t.to_dict() for h, t in self.tasks.items()})

    def __repr__(self):
        all_tasks = "\n".join([f"{h}: {t}" for h, t in self.tasks.items()])
        return all_tasks
