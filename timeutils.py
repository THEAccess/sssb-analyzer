from datetime import datetime, timedelta, time
from typing import List

from params import disk_time_format


def closest_day(wk_index: int, hour: int, minute: int):
    """
        This function returns the date and time of a weekday with the specified hour and minute.

        Args:
            wk_index (int): The index of the weekday, where Monday is 0 and Sunday is 6.
            hour (int): The hour for the desired time.
            minute (int): The minute for the desired time.

        Returns:
            datetime.datetime: The next date and time of the desired weekday with the specified hour and minute.
        """
    # Get the current date and time
    now = datetime.now()

    # Calculate the next Monday and next Thursday
    next_monday = now + timedelta(days=(7 - now.weekday()) % 7)
    next_monday = next_monday.replace(hour=16, minute=0, second=0, microsecond=0)
    if now > next_monday:
        next_monday += timedelta(days=7)
    next_thursday = now + timedelta(days=(3 - now.weekday()) % 7)
    if now > next_thursday:
        next_thursday += timedelta(days=7)
    next_thursday = next_thursday.replace(hour=10, minute=0, second=0, microsecond=0)

    # Calculate the time difference between now and each of the next times
    monday_diff = abs(next_monday - now)
    thursday_diff = abs(next_thursday - now)

    # Return the next time that is closest to the current time
    if monday_diff < thursday_diff:
        return next_monday
    else:
        return next_thursday


def next_closest_SSSB_closing_time():
    """
        This function returns the date and time of the next Monday at 16:00 or Thursday at 10:00, whichever is closest.

        Returns:
            datetime.datetime: The next date and time of either Monday at 16:00 or Thursday at 10:00, whichever is closest.
        """
    # Calculate the next Monday at 16:00.
    next_monday_16 = closest_day(0, 16, 0)
    # Calculate the next Thursday at 10:00.
    next_thursday_10 = closest_day(3, 10, 0)
    # Return whichever of the two dates is closest.
    if next_monday_16 < next_thursday_10:
        return next_monday_16
    else:
        return next_thursday_10


def is_next_SSSB_closing_time_near(minutes):
    now = datetime.now()
    # Calculate the next Monday at 16:00.
    next_monday_16 = closest_day(0, 16, 0)
    # Calculate the next Thursday at 10:00.
    next_thursday_10 = closest_day(3, 10, 0)
    # Calculate the difference between now and the next Monday at 16:00 in minutes.
    monday_diff = abs((next_monday_16 - now).total_seconds() / 60)
    # Calculate the difference between now and the next Thursday at 10:00 in minutes.
    thursday_diff = abs((next_thursday_10 - now).total_seconds() / 60)
    # Return true if the either Monday at 16:00 or Thursday at 10:00 is less than x minutes away
    return min(monday_diff, thursday_diff) <= minutes


def get_time_range(dates: List[str]):
    dates = [datetime.strptime(date, disk_time_format) for date in dates]
    dates.sort()
    return (dates[-1] - dates[0]).days
