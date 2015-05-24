#!/usr/bin/env python

from datetime import date, timedelta


def is_weekday(date):
    """
    Returns True or False depending on whether a given datetime.date is a
    weekday (Monday to Friday).
    """
    # The weekday() method sets Monday as 0, Sunday as 6
    return (date.weekday() in range(4))


def previous_day(date, skip_weekends):
    """
    Returns the previous day. Takes a datetime.date object.

    If skip_weekends is True, then the day before a Friday is the preceding
    Monday.
    """
    if skip_weekends:
        while not is_weekday(date):
            date -= timedelta(1)
        return date
    else:
        date -= timedelta(1)
        return date


def next_day(date, skip_weekends):
    """
    Returns the next day as a datetime.date object.

    If skip_weekends is True, then the day after a Friday is the following
    Monday.
    """
    if skip_weekends:
        while not is_weekday(date):
            date += timedelta(1)
        return date
    else:
        date += timedelta(1)
        return date


def weekday_initials():
    """
    Returns a list of abbreviations for the days of the week, starting with
    Sunday.
    """
    # Get a week's worth of date objects
    week = [date.today() + timedelta(i) for i in range(7)]

    # Sort them by weekday(), and rearrange to put Sunday first
    week = sorted(week, key=lambda day: day.weekday())
    week.insert(0, week.pop())

    # Get the locale's abbreviated name
    days = [day.strftime("%a") for day in week]

    # Now we want to reduce these to minimal unique abbreviations. For each day
    # of the week, start with the first letter, and keep adding letters until
    # we have a unique abbreviation.
    short_days = []
    for idx in range(7):
        full_day = days[idx]
        length = 1

        while len([day for day in days
                       if day[:length] == full_day[:length]
                       and day != days[idx]]) > 0:
            length += 1

        short_days.append(full_day[:length])

    return short_days