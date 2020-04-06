from .task import Task
from .tag import parse_tag
from typing import List
import parse
import hashlib

class TaskDB:
    def __init__(self, filename: str = None):
        self.tasks = {}
        if filename:
            self.filename = filename
            self.load_tasks()

    def load_tasks(self):
        with open(self.filename, "r") as f:
            for entry in f.readlines():
                self.add_task(entry, with_hash=True)

    def save_tasks(self):
        with open(self.filename, "w") as f:
            f.write(str(self))

    def add_task(self, entry: str, with_hash=False):
        if with_hash:
            r = parse.parse("{hash:4x} {entry}", entry)
            t = Task(r['entry'])
            self.tasks[r['hash']] = t
        else:
            salt = 0
            while (hash := self._hash(entry, salt)) in self.tasks.keys():
                salt += 1
            t = Task(entry)
            self.tasks[hash] = t
        return t

    def _hash(self, entry: str,  salt: int) -> int:
        salt = str(salt).encode()
        return int(
            hashlib.blake2b(entry.encode(), digest_size=2, salt=salt).hexdigest(),
            base=16,
        )


    def remove_task(self, hash: int):
        self.tasks.pop(hash)

    def __repr__(self):
        sorted_tasks = sorted(
            self.tasks.items(), key=lambda x: x[0] + (0x10000 if x[1].done else 0)
        )
        format_hash = lambda h: f"{hex(h).lstrip('0x').zfill(4)}"
        all_tasks = "\n".join([f"{format_hash(x[0])} {x[1]}" for x in sorted_tasks])
        return all_tasks

