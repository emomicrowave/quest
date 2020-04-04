import pytest
import hashlib
from dataclasses import dataclass

from context import kobold
from kobold.task import Task, PrettyTask
from kobold.tag import Tag

example_task_str = "54a5 example"
example_task = {
    "entry": "example",
    "hash": int("54a5", base=16),
}
hash_hash = int("1936", base=16)
stylized_output = (
    "\x1b[31mbea1\x1b[0m example \x1b[32m+example\x1b[0m \x1b[34m@example\x1b[0m"
)


class TestTaskCreate:
    def test_create_empty_task(self):
        with pytest.raises(ValueError):
            t = Task("")

    def test_create_simple_task(self):
        entry = "example"
        t = Task(entry)
        assert t.entry == example_task["entry"] and t.hash == example_task["hash"]

    def test_create_hashed_task(self):
        entry = "54a5 example"
        t = Task(entry)
        assert t.entry == example_task["entry"] and t.hash == example_task["hash"]

    def test_create_only_hashy(self):
        entry = "54a5"
        t = Task(entry)
        assert t.entry == entry and t.hash == hash_hash


class TestTaskTags:
    def test_single_project_tag(self):
        entry = "0000 example +project_tag"
        t = Task(entry)
        assert t.tags == [Tag("project", "project_tag")]

    def test_multiple_project_tags(self):
        entry = "there +are interleaved +project +tags"
        t = Task(entry)
        assert t.tags == [
            Tag("project", "are"),
            Tag("project", "project"),
            Tag("project", "tags"),
        ]

    def test_single_context_tag(self):
        entry = "0000 example @context_tag"
        t = Task(entry)
        assert t.tags == [Tag("context", "context_tag")]

    def test_multiple_context_tags(self):
        entry = "there @are interleaved @context @tags"
        t = Task(entry)
        assert t.tags == [
            Tag("context", "are"),
            Tag("context", "context"),
            Tag("context", "tags"),
        ]


class TestTaskRepr:
    def test_simple_task(self):
        t = Task("example")
        assert str(t) == example_task_str

    def test_stylized_task(self):
        t = PrettyTask(Task("example +example @example"))
        assert str(t) == stylized_output
