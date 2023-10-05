from typing import Union
from datetime import datetime

def pretty_datetime(date: Union[str, datetime]) -> str:
    if isinstance(date, str):
        date, time = date.split(" ")
        year, month, day = date.split("-")
        time, milis = time.split(".")
        hour, minute, sec = time.split(":")
        return f"{day}. {month}. {year}, {hour}:{minute}:{sec}"
    elif isinstance(date, datetime):
        minute = str(date.minute).ljust(2, "0")
        second = str(date.second).ljust(2, "0")
        return f"{date.day}. {date.month}. {date.year}, {date.hour}:{minute}:{second}"