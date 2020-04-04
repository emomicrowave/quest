from pathlib import Path
from context import kobold
from kobold.task_db import TaskDB, PrettyTaskDB

empty_db_path = Path(__file__).parent.joinpath("dbs/empty_db.kob")
simple_db_path = Path(__file__).parent.joinpath("dbs/simple_db.kob")
simple_db_content = "0001 task 1 +dbtest @pytest\n0002 task 2 +dbtest @pytest +second_test\nbeef task 3 +deadbeef"
simple_db_content_pretty = (
    "\x1b[31m0001\x1b[0m task 1 \x1b[32m+dbtest\x1b[0m \x1b[34m@pytest\x1b[0m\n"
    + "\x1b[31m0002\x1b[0m task 2 \x1b[32m+dbtest\x1b[0m \x1b[34m@pytest\x1b[0m \x1b[32m+second_test\x1b[0m\n"
    + "\x1b[31mbeef\x1b[0m task 3 \x1b[32m+deadbeef\x1b[0m"
)

example_task_str = "54a5 example"
example_task = {
    "entry": "example",
    "hash": int("c150", base=16),
}

with open(simple_db_path, "w") as f:
    f.write(simple_db_content)


class TestTaskDBOpen:
    def test_open_empty_taskdb(self):
        tdb = TaskDB(empty_db_path)
        assert tdb.filename == empty_db_path and len(tdb.tasks) == 0
        tdb.save_tasks()
        with open(empty_db_path) as f:
            assert len(f.read()) == 0

    def test_open_simple_taskdb(self):
        tdb = TaskDB(simple_db_path)
        assert len(tdb.tasks) == 3
        assert tdb.tasks[0x0001].entry == "task 1 +dbtest @pytest"
        assert tdb.tasks[0x0002].entry == "task 2 +dbtest @pytest +second_test"
        assert tdb.tasks[0xBEEF].entry == "task 3 +deadbeef"
        with open(simple_db_path) as f:
            assert str(tdb) == f.read()


class TestTaskDBSave:
    def test_save_empty_to_simple(self):
        tdb = TaskDB(empty_db_path)
        tdb.add_task(example_task["entry"])
        tdb.add_task(example_task["entry"])
        assert tdb.tasks[example_task["hash"]].entry == example_task["entry"]


class TestTaskDBRemove:
    def test_remove_tasks(self):
        tdb = TaskDB(simple_db_path)
        tdb.remove_task(0xBEEF)
        with open(simple_db_path) as f:
            assert str(tdb) == "".join(f.readlines()[:-1]).strip()


class TestPrettyTaskDBRepr:
    def test_pretty_db(self):
        tdb = PrettyTaskDB(TaskDB(simple_db_path))
        assert str(tdb) == simple_db_content_pretty
