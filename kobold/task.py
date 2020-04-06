from .tag import ctags, utags, ptags, parse_tag, Tag

class Task:
    def __init__(self, entry: str):
        if len(entry) == 0:
            error_msg = "Your entry is empty! You can't complete a task if there's no task to complete"
            raise ValueError(error_msg)
        self.entry = entry

    @property
    def done(self):
        return self.entry.startswith("[X]")

    def complete(self):
        if not self.done:
            self.entry = f"[X] {self.entry}"

    @property
    def tags(self):
        tags = []
        tags += [r["tag"] for r in ptags.findall(self.entry)]
        tags += [r["tag"] for r in ctags.findall(self.entry)]
        tags += [r["tag"] for r in utags.findall(self.entry)]
        return tags

    def iterwords(self):
        yield from (parse_tag(word) for word in self.entry.split())

    def __repr__(self):
        return self.entry

