from .task import Task
import arrow


def completed_today(t: Task) -> bool:
    if not t.state == "done":
        return False
    now = arrow.now().isocalendar()
    task = arrow.get(t.completed).isocalendar()
    return now == task


def completed_this_week(t: Task) -> bool:
    if not t.state == "done":
        return False
    now = arrow.now().isocalendar()[:2]
    task = arrow.get(t.completed).isocalendar()[:2]
    return now == task


def due_today(t: Task) -> bool:
    if not t.due:
        return False
    now = arrow.now().isocalendar()
    task = arrow.get(t.due).isocalendar()
    return now == task


def due_this_week(t: Task) -> bool:
    if not t.due:
        return False
    now = arrow.now().isocalendar()[:2]
    task = arrow.get(t.due).isocalendar()[:2]
    return now == task


def todo(t: Task) -> bool:
    return not t.state == "done"
