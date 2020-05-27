from yaml import load, Loader
from pathlib import Path
from context import kobold
from kobold.taskdb import TaskDB
from kobold.task import Task


def test_open_empty_taskdb():
    db = TaskDB({})
    assert db.tasks == {}

def test_add():
    db = TaskDB({})
    task = Task(name="test", created="now")
    db.add(task)
    assert list(db.tasks.values()) == [Task(name="test", created="now")]

def test_add_same_task():
    db = TaskDB({})
    task = Task(name="test", created="now")
    db.add(task)
    db.add(task)
    hashes = list(db.tasks.keys())
    assert all(t == task for t in db.tasks.values())
    assert hashes[0] != hashes[1]

def test_remove_task():
    db = TaskDB({})
    task = Task(name="test", created="now")
    db.add(task)
    assert len(db.tasks) == 1
    hash = list(db.tasks.keys())[0]
    db.pop(hash)
    assert db.tasks == {}

def test_repr():
    db = TaskDB({})
    db.tasks = {"dead": Task(name="test", created="now")}
    assert db.__repr__() == "dead: void: test"
