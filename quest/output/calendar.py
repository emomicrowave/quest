from .lists import format_tdb
from .. import filters
from ..taskdb import TaskDB
from ..task import Task

from arrow import Arrow
from rich import print, box
from rich.table import Table, Column
from rich.text import Text
from typing import List, Tuple

weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def calendar(tdb: TaskDB, period="month") -> None:
    assert period in ["month", "week"]
    date = Arrow.now()
    tasks = _calendar_tasks(tdb, date, period)
    _calendar_print(tasks, date)


def _calendar_print(tasks: List[Tuple[Arrow, TaskDB]], date: Arrow) -> None:
    cols = [Column(f"{d}", justify="left") for d in weekdays]
    table = Table(*cols, title=date.format("MMMM"), box=box.MINIMAL, show_lines=True)
    today = (
        lambda d: "bold yellow"
        if d.isocalendar() == date.isocalendar()
        else "white"
        if d.month == date.month
        else "bright_black"
    )
    format = lambda date, db: Text("\n").join(
        [Text(f"{date.day}          ", style=today(date)), format_tdb(db, False, False)]
    )
    days = [format(date, db) for date, db in tasks]
    weeks = [days[i : i + 7] for i in range(0, len(days), 7)]
    for w in weeks:
        table.add_row(*w)
    print(table)


def _calendar_tasks(tdb: TaskDB, date: Arrow, period) -> List[Tuple[Arrow, TaskDB]]:
    start, end = _calendar_range(date, period)
    tasks = []  # type: List[Tuple[Arrow, TaskDB]]
    for date in Arrow.range("day", start, end):
        tasks.append((date, tdb.filter(lambda t: filters.due_on(t, date))))
    return tasks


def _calendar_range(date: Arrow, period) -> Tuple[Arrow, Arrow]:
    start = date.floor(period).floor("week")
    end = date.ceil(period).ceil("week")
    return start, end
