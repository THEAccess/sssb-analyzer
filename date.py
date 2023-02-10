import datetime


def closest_day(wk_index: int, hour: int, minute: int):
    today = datetime.datetime.now()
    next_monday = today + datetime.timedelta((7 + wk_index - today.weekday()) % 7)
    return datetime.datetime.combine(next_monday, datetime.time(hour, minute))


def closest_monday_16_or_thursday_10():
    next_monday_16 = closest_day(0, 16, 0)
    next_tuesday_10 = closest_day(3, 10, 0)
    if next_monday_16 < next_tuesday_10:
        return next_monday_16
    else:
        return next_tuesday_10
