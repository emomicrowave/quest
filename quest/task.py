import arrow
from parse import findall
from typing import Dict


class Task:
    def __init__(
        self,
        name: str,
        project: str = "void",
        context: str = None,
        state: str = "todo",
        xp: int = 1,
        created: str = None,
        completed: str = None,
        due: str = None,
    ):
        if len(name) == 0:
            error_msg = "Your entry is empty! You can't complete a task if there's no task to complete"
            raise ValueError(error_msg)
        self.name = name
        self.project = project
        self.state = state
        self.context = context
        self.xp = xp
        self.created = created or arrow.now().format("YYYY-MM-DDTHH:mm")
        self.completed = completed
        self.due = due

    @property
    def done(self) -> bool:
        return self.state == "done"

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str):
        assert value in ["todo", "in_progress", "done"]
        if value == "done":
            self.completed = arrow.now().format("YYYY-MM-DDTHH:mm")
        self._state = value

    def to_dict(self) -> Dict:
        return {k.lstrip("_"): v for k, v in self.__dict__.items() if v is not None}

    def __str__(self):
        return f"{self.project}: {self.name}"

    def __repr__(self):
        return f"Task: {self.name=} {self.project=} {self.state=}"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
