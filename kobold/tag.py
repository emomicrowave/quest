import parse
from dataclasses import dataclass


@dataclass
class Tag:
    type: str
    value: str

    def __repr__(self):
        return f"{self.type}:{self.value}"


@parse.with_pattern(r"\S+:\S+")
def parse_utag(text):
    return Tag(*text.split(":"))


@parse.with_pattern(r"\+\S+")
def parse_ptag(text):
    return Tag("project", text.lstrip("+"))


@parse.with_pattern(r"@\S+")
def parse_ctag(text):
    return Tag("context", text.lstrip("@"))


ptags = parse.compile("{tag:Tag}", dict(Tag=parse_ptag))
ctags = parse.compile("{tag:Tag}", dict(Tag=parse_ctag))
utags = parse.compile("{tag:Tag}", dict(Tag=parse_utag))


def parse_tag(text: str, default=None):
    if result := ptags.parse(text):
        return result["tag"]
    elif result := ctags.parse(text):
        return result["tag"]
    elif result := utags.parse(text):
        return result["tag"]
    else:
        return default
