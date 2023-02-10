from datetime import datetime, timedelta, time


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
    today = datetime.now()
    # Calculate the next weekday using the weekday index, using the modulo operator to handle cases where the target
    # weekday is earlier in the week than today.
    next_monday = today + timedelta((7 + wk_index - today.weekday()) % 7)
    # Combine the date of the next weekday with the specified hour and minute to get the final date and time.
    return datetime.combine(next_monday, time(hour, minute))


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
    monday_diff = (next_monday_16 - now).total_seconds() / 60
    # Calculate the difference between now and the next Thursday at 10:00 in minutes.
    thursday_diff = (next_thursday_10 - now).total_seconds() / 60
    # Return true if the either Monday at 16:00 or Thursday at 10:00 is less than x minutes away
    return min(monday_diff, thursday_diff) <= minutes
