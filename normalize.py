from datetime import datetime
from typing import List, Tuple

from defs import Table


def normalize(data: List[Tuple[Table, datetime]]) -> List[Table]:
    dates = [date for _, date in data]
    dates.sort()
    min_date = dates[0]
    max_date = dates[-1]
    range = (dates[-1] - dates[0]).days
    for table, date in data:
        days_offset = (max_date - date).days
        if days_offset != 0:
            normalize_day(table, days_offset)
    return [table for table, _ in data]


def normalize_day(table: Table, days_offset: int):
    for row in table:
        row[2] = row[2] + days_offset
