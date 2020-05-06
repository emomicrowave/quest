import pytest
from dataclasses import dataclass

from context import kobold
from kobold.task import Task


class TestTaskCreate:
    def test_create_empty_task(self):
        with pytest.raises(ValueError):
            t = Task("")

    def test_not_done(self):
        t = Task(name="test", project="test", state="todo", created="now", due="tomorrow")
        assert not t.done

    def test_complete(self):
        t = Task(name="test", project="test", state="todo", created="now", due="tomorrow")
        t.complete()
        assert t.done

    def test_project(self):
        t = Task(name="test", project="test_project", state="todo", created="now", due="tomorrow")
        assert t.project == "test_project"

    def test_repr_defined(self):
        t = Task(name="test")
        assert type(t.__repr__()) == str


