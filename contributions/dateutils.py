#!/usr/bin/env python

import datetime


def _today():
    """
    Wrapper function for getting the current date. Broken into its own function
    for easier mocking.
    """
    return datetime.date.today()


def is_weekday(date):
    """
    Returns True if a given datetime.date is a weekday (Monday to Friday).
    """
    # The weekday() method returns the day of the week as an integer, where
    # Monday is 0 and Sunday is 6. Weekdays are thus 0-4 (inclusive).
    return (date.weekday() in range(5))


def is_within_last_year(date):
    """
    Returns True if a date falls within the last year.

    Takes a datetime.date as an argument.
    """
    today = _today()
    one_year_ago = datetime.date(today.year - 1, today.month, today.day)
    if one_year_ago <= date <= today:
        return True

    # Catch a trailing Saturday in the first column, and display it anyway
    elif date.weekday() == 5 and date == one_year_ago - datetime.timedelta(1):
        return True
    else:
        return False


def _increment_day(date, skip_weekends, val):
    """
    Increments a datetime.date object by +/-1 day depending on val.

    If skip_weekends is True, then it treats Friday and Monday as consecutive
    days.
    """
    date += val * datetime.timedelta(1)
    if skip_weekends:
        while not is_weekday(date):
            date += val * datetime.timedelta(1)
    return date


def previous_day(date, skip_weekends):
    """
    Returns the previous day. Takes a datetime.date object.

    If skip_weekends is True, then the day before a Friday is the preceding
    Monday.
    """
    return _increment_day(date, skip_weekends, -1)


def next_day(date, skip_weekends):
    """
    Returns the next day as a datetime.date object.

    If skip_weekends is True, then the day after a Friday is the following
    Monday.
    """
    return _increment_day(date, skip_weekends, +1)


def weekday_initials():
    """
    Returns a list of abbreviations for the days of the week, starting with
    Sunday.
    """
    # Get a week's worth of date objects
    week = [_today() + datetime.timedelta(i) for i in range(7)]

    # Sort them so that Sunday is first
    week = sorted(week, key=lambda day: (day.weekday() + 1) % 7)

    # Get the abbreviated names of the weekdays
    day_names = [day.strftime("%a") for day in week]

    # Now reduce the names to minimal unique abbreviations (in practice, this
    # means one or two-letter abbreviations).
    short_names = []

    # For each day of the week, start with the first letter, and keep adateing
    # letters until we have a unique abbreviation.
    for idx in range(7):
        day_name = day_names[idx]
        length = 1

        # This list comprehension finds collisions: other day names which match
        # the first (length) characters of this day.
        while [day for day in day_names
                   if day[:length] == day_name[:length]
                   and day != day_name]:
            length += 1

        short_names.append(day_name[:length])

    return short_names


def past_date_str(date):
    """
    Given a date in the past, return a human-readable string explaining how
    long ago it was.
    """
    if date > _today():
        raise ValueError("Date {} is in the future, not the past".format(date))

    difference = (_today() - date).days

    # I'm treating a month as ~30 days. This may be a little inaccurate in some
    # months, but it's good enough for our purposes.
    if difference == 1:
        return "a day ago"
    elif difference < 30:
        return "%d days ago" % difference
    elif difference < 30 * 2:
        return "a month ago"
    elif difference < 366:
        return "%d months ago" % (difference / 30)
    else:
        return "more than a year ago"
