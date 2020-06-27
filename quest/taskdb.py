from .task import Task
import hashlib
import yaml
import arrow
import xdg
from typing import Union, Dict, Tuple, Callable
from pathlib import Path


class TaskDB:
    def __init__(self, tasks: Dict = None):
        tasks = tasks or dict()
        self.tasks = {
            k: (v if isinstance(v, Task) else Task(**v)) for k, v in tasks.items()
        }

    def add(self, task: Task) -> Tuple[Task, str]:
        salt = 0
        while (hash := self._hash(str(task), bytes([salt]))) in self.tasks.keys():
            salt += 1
        self.tasks[hash] = task
        return task, hash

    def pop(self, hash: str) -> Tuple[Task, str]:
        return self.tasks.pop(hash), hash

    def filter(self, predicate: Callable[[Task], bool]):
        tasks = {k: t for k, t in self.tasks.items() if predicate(t)}
        return TaskDB(tasks)

    @property
    def xp(self) -> int:
        return int(sum([t.xp for h, t in self]))

    def __len__(self) -> int:
        return len(self.tasks)

    def __getitem__(self, index) -> Task:
        return self.tasks[index]

    def __iter__(self):
        t = lambda s, m: arrow.get(s).timestamp + (10 ** 10 * m) if s else 0
        keyer = (
            lambda x: -t(x[1].completed, -2)
            if x[1].state == "done"
            else t(x[1].due, 0) or t(x[1].created, 1)
        )
        yield from ((h, t) for h, t in sorted(self.tasks.items(), key=keyer))

    def _hash(self, entry: str, salt: bytes) -> str:
        hash = int(
            hashlib.blake2b(entry.encode(), digest_size=2, salt=salt).hexdigest(),
            base=16,
        )
        return hex(hash).lstrip("0x").zfill(4)

    def __repr__(self):
        all_tasks = "\n".join([f"{h}: {t}" for h, t in self.tasks.items()])
        return all_tasks


class YamlDB:
    """
    Creates a TaskDB instance based on a yaml file.

    Serves as a context manager, which returns a TaskDB instance. If opened in
    write mode, the context manager will convert and write the returned TaskDB
    instance to the original yaml file.
    """

    def __init__(self, filename: str, mode: str = "r"):
        """
        Filename should point to valid yaml file. Mode can either be "r" or "w".
        """
        assert mode in "rw"
        self.filename = filename
        self.mode = mode
        self.create_if_nonexistant(filename)

    def create_if_nonexistant(self, filename):
        p = Path(filename)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch(exist_ok=True)

    def backup(self, content):
        """
        Create a backup of the yaml file in XDG data share.
        """
        backup_name = (
            xdg.XDG_DATA_HOME
            / "quest"
            / f"quest_backup_{arrow.now().format('YYYY-MM-DDTHH-mm-ss')}"
        )
        self.create_if_nonexistant(backup_name)
        with open(backup_name, "w") as f:
            f.write(content)

    def __enter__(self) -> TaskDB:
        """
        Returns TaskDB from yaml file. Creates a backup if in write mode and
        before content is changed.
        """
        with open(self.filename, "r") as f:
            tasks = yaml.load(f, Loader=yaml.Loader)
            f.seek(0)
            content = f.read()
        if self.mode == "w":
            self.backup(content)
        self.taskdb = TaskDB(tasks)
        return self.taskdb

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Writes the contained TaskDB to the yaml file if in write mode.
        """
        if exc_type is None and self.mode == "w":
            with open(self.filename, "w") as f:
                as_yaml = yaml.dump(
                    {h: t.to_dict() for h, t in self.taskdb.tasks.items()}
                )
                f.writelines(as_yaml)
