from yaml import load, Loader
from pathlib import Path
from context import kobold
from kobold import Task, TaskDB


def test_open_empty_taskdb():
    """
    Empty database has a length of 0.
    """
    db = TaskDB()
    assert len(db) == 0


def test_add():
    """
    Add a task to db.
    """
    db = TaskDB()
    task = Task(name="test", created="now")
    db.add(task)
    assert list(db.tasks.values()) == [Task(name="test", created="now")]


def test_add_same_task():
    """
    Hash collisions are handled.
    """
    db = TaskDB()
    task = Task(name="test", created="now")
    db.add(task)
    db.add(task)
    hashes = list(db.tasks.keys())
    assert all(t == task for t in db.tasks.values())
    assert hashes[0] != hashes[1]


def test_remove_task():
    """
    Removing based on hash.
    """
    db = TaskDB()
    task = Task(name="test", created="now")
    db.add(task)
    assert len(db) == 1
    hash = list(db.tasks.keys())[0]
    db.pop(hash)
    assert len(db) == 0


def test_repr():
    """
    __repr__ should return one line per task.
    """
    db = TaskDB()
    db.add(Task("test"))
    assert len(db.__repr__().splitlines()) == 1
    db.add(Task("test"))
    assert len(db.__repr__().splitlines()) == 2
    db.add(Task("test"))
    db.add(Task("test"))
    db.add(Task("test"))
    assert len(db.__repr__().splitlines()) == 5


def test_filter():
    """
    Filtering by predicate works.
    """
    db = TaskDB()
    db.add(Task("test 1", state="done"))
    db.add(Task("test2 ", state="todo"))
    db = db.filter(lambda t: t.state == "todo")
    assert len(db) == 1


def test_access_by_hash():
    """
    Does db[hash] access work? db.tasks is a standard dict, so we use it to get a key.
    """
    db = TaskDB()
    t = Task("test 1", state="done")
    db.add(t)
    hash = list(db.tasks.keys())[0]
    assert db[hash] == t


def test_iter():
    """
    Iterating over a TaskDB has a specific order. Ensure it is kept.
    """
    db = TaskDB()
    t1 = Task("test 1", state="done", completed="2020-01-01")
    db.add(t1)
    t2 = Task("test 2", state="done", completed="2020-02-01")
    db.add(t2)
    t3 = Task("test 3", state="todo", due="2020-03-01")
    db.add(t3)
    t4 = Task("test 4", state="todo")
    db.add(t4)
    assert [t for _h, t in db] == [t3, t4, t2, t1]
