import pytest
from dataclasses import dataclass

from context import kobold
from kobold.task import Task
from kobold.tag import Tag


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

    def test_iterwords(self):
        entry = "example +example @example ex:example"
        expected = [
                Tag("word", "example"),
                Tag("project", "example"),
                Tag("context", "example"),
                Tag("ex", "example"),
                ]
        t = Task(entry)
        assert list(t.iterwords()) == expected


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
        entry = "example"
        t = Task(entry)
        assert str(t) == entry

