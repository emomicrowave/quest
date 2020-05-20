from datetime import datetime

STANDARD_FORMAT = "%Y-%m-%dT%H:%M"

def parse_standard_format(entry: str) -> datetime:
    try:
        return datetime.strptime(entry, STANDARD_FORMAT)
    except ValueError:
        return None
