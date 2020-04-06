import typer
import hashlib
import parse
from .tag import ctags, utags, ptags, parse_tag, Tag

with_hash = parse.compile("{hash:4x} {text}").parse
no_hash = parse.compile("{text}").parse


class Task:
    def __init__(self, entry: str, salt=b"", hash=None):
        if len(entry) == 0:
            error_msg = "Your entry is empty! You can't complete a task if there's no task to complete"
            raise ValueError(error_msg)

        self.entry = entry
        self.hash = hash or self._hash(salt)

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

    def _hash(self, salt):
        return int(
            hashlib.blake2b(self.entry.encode(), digest_size=2, salt=salt).hexdigest(),
            base=16,
        )

    def iterwords(self):
        iterator = (word for word in str(self).split())
        yield Tag("hash", next(iterator))
        yield from (parse_tag(word) for word in iterator)

    def __repr__(self):
        hash = hex(self.hash).lstrip("0x").zfill(4)
        return f"{hash} {self.entry}"


class PrettyTask(Task):
    def __init__(self, t: Task):
        super().__init__(t.entry, hash=t.hash)

    def __repr__(self):
        if self.done:
            return typer.style(super().__repr__(), fg=typer.colors.BRIGHT_BLACK)
        else:
            hash = typer.style(
                hex(self.hash).lstrip("0x").zfill(4), fg=typer.colors.RED
            )
            return " ".join([hash] + [self.stylize(w) for w in self.entry.split()])

    def stylize(self, word: str):
        if word.startswith("+"):
            return typer.style(word, fg=typer.colors.GREEN)
        elif word.startswith("@"):
            return typer.style(word, fg=typer.colors.BLUE)
        elif parse.parse("{:S}:{:S}", word):
            return typer.style(word, fg=typer.colors.YELLOW)
        else:
            return word
