import pytest
from dataclasses import dataclass

from quest import Task


def test_not_done():
    t = Task(name="test", project="test", state="todo", created="now", due="tomorrow")
    assert not t.done


def test_project():
    t = Task(
        name="test", project="test_project", state="todo", created="now", due="tomorrow"
    )
    assert t.project == "test_project"


def test_repr_defined():
    t = Task(name="test")
    assert type(t.__repr__()) == str
