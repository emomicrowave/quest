from .task import Task
import arrow
import functools


def due_guard(func):
    """
    Decorator. Returns False if task doesn't have due date.
    """

    @functools.wraps(func)
    def _due_guard(t: Task, *args, **kwargs):
        if not t.due:
            return False
        return func(t, *args, **kwargs)

    return _due_guard


def done_guard(func):
    """
    Decorator. Returns False if task's state is not "done".
    """

    @functools.wraps(func)
    def _done_guard(t: Task, *args, **kwargs):
        if not t.state == "done":
            return False
        return func(t, *args, **kwargs)

    return _done_guard


@done_guard
def completed_today(t: Task) -> bool:
    """
    Task completion date is today.
    """
    now = arrow.now().isocalendar()
    task = arrow.get(t.completed).isocalendar()
    return now == task


@done_guard
def completed_this_week(t: Task) -> bool:
    """
    Task completion date is in the current calendar week.
    """
    now = arrow.now().isocalendar()[:2]
    task = arrow.get(t.completed).isocalendar()[:2]
    return now == task


@due_guard
def due_today(t: Task) -> bool:
    """
    Task due date is today.
    """
    now = arrow.now().isocalendar()
    task = arrow.get(t.due).isocalendar()
    return now == task


@due_guard
def due_this_week(t: Task) -> bool:
    """
    Task due date is in the current calendar week.
    """
    now = arrow.now().isocalendar()[:2]
    task = arrow.get(t.due).isocalendar()[:2]
    return now == task


@due_guard
def overdue(t: Task) -> bool:
    """
    Task due date is in the past.
    """
    return arrow.now().isocalendar() > arrow.get(t.due).isocalendar()


def todo(t: Task) -> bool:
    """
    Task is not done.
    """
    return not t.state == "done"


@due_guard
def due_remaining(t: Task, days: int) -> bool:
    """
    At least DAYS remaining until T due date.
    """
    rem = arrow.get(t.due) - arrow.now()
    return rem.days >= days
