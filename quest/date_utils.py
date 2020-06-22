import arrow

weekdays = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


def parse_date(date: str) -> str:
    """
    Accepts either a YYYY-MM-DD[THH-mm] date, a weekday or one of: ['today', '.', 'tomorrow', 'eow', 'eom'].

    The latter are converted to the former format so that they can be parsed as an Arrow object.
    """
    try:
        if date in ["today", "."]:
            date = arrow.now().format("YYYY-MM-DD")
        elif date == "tomorrow":
            date = arrow.now().shift(days=1).format("YYYY-MM-DD")
        elif date == "eow":
            date = arrow.now().ceil("week").format("YYYY-MM-DD")
        elif date == "eom":
            date = arrow.now().ceil("month").format("YYYY-MM-DD")
        elif date.lower() in weekdays:
            date = arrow.now().shift(weekday=weekdays[date]).format("YYYY-MM-DD")
    finally:
        return date


def humanize(date: str) -> str:
    """
    Accepts a valid date string and returns a human readable date spec.

    Example:
    # now = 2020-01-01
    humanize("2020-01-01")
    "today"

    humanize("2020-01-02")
    "tomorrow"

    humanize("2020-01-03")
    "in 2 days"
    """
    date = arrow.get(date).ceil("day")
    now = arrow.now().ceil("day")

    diff = (date - now).days

    if diff == 0:
        readable = "today"
    elif diff == 1:
        readable = "tomorrow"
    elif diff == -1:
        readable = "yesterday"
    elif 0 <= diff <= 7:
        readable = f"{date.humanize(granularity=['day'])} ({date.format('ddd')})"
    else:
        readable = date.humanize(granularity=["day"])
    return readable
