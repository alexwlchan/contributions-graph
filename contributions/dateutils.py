#!/usr/bin/env python

import datetime


def today():
    """
    Gets the current date. Wrapper function to make it easier to stub out in
    tests.
    """
    return datetime.date.today()


def start():
    """
    Gets the date from one year ago, which is the start of the contributions
    graph.
    """
    return datetime.date(today().year - 1, today().month, today().day)


def display_date(date):
    """
    Returns a long date string. Example output: "May 24, 2015".
    """
    return date.strftime("%B %d, %Y").replace(" 0", " ")


def previous_day(date):
    """
    Returns the previous day as a datetime.date object.
    """
    return date - datetime.timedelta(1)


def next_day(date):
    """
    Returns the next day as a datetime.date object.
    """
    return date + datetime.timedelta(1)


def elapsed_time(date):
    """
    Given a date in the past, return a human-readable string explaining how
    long ago it was.
    """
    if date > today():
        raise ValueError("Date {} is in the future, not the past".format(date))

    difference = (today() - date).days

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

def weekday_initials():
    """
    Returns a list of abbreviations for the days of the week, starting with
    Sunday.
    """
    # Get a week's worth of date objects
    week = [today() + datetime.timedelta(i) for i in range(7)]

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
