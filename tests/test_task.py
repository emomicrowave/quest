import pytest
from dataclasses import dataclass

from context import kobold
from kobold.task import Task


class TestTaskCreate:
    def test_create_empty_task(self):
        with pytest.raises(ValueError):
            t = Task("")

    def test_create_simple_task(self):
        entry = "example"
        t = Task(entry)
        assert t.entry == entry

    def test_create_done_task(self):
        entry = "[X] example"
        t = Task(entry)
        assert t.done

    def test_create_and_complete_task(self):
        entry = "example"
        t = Task(entry)
        assert not t.done
        t.complete()
        assert t.done


class TestTaskRepr:
    def test_simple_task(self):
        entry = "example"
        t = Task(entry)
        assert str(t) == entry
