from parse import findall


class Task:
    def __init__(self, entry: str):
        if len(entry) == 0:
            error_msg = "Your entry is empty! You can't complete a task if there's no task to complete"
            raise ValueError(error_msg)
        self.entry = entry

    @property
    def done(self) -> bool:
        return self.entry.startswith("[X]")

    @property
    def project(self) -> str:
        result = list(findall(r" +{project:w}", self.entry))
        if len(result) != 0:
            return result[0]['project']

    def complete(self) -> None:
        if not self.done:
            self.entry = f"[X] {self.entry}"

    def __repr__(self):
        return self.entry
