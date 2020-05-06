from parse import findall
from datetime import datetime


class Task:
    def __init__(self, name: str, project: str = "void", state: str = "todo", created: str = None, due: str = None):
        if len(name) == 0:
            error_msg = "Your entry is empty! You can't complete a task if there's no task to complete"
            raise ValueError(error_msg)
        self.name = name
        self.project = project
        self.state = state
        self.created = created or datetime.now().strftime("%Y-%m-%dT%H:%M")
        self.due = due

    @property
    def done(self) -> bool:
        return self.state == "done"

    @property
    def dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def complete(self) -> None:
        self.state = "done"

    def __str__(self):
        return f"{self.project}: {self.name}"

    def __repr__(self):
        return f"Task: {self.name=} {self.project=} {self.state=}"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
