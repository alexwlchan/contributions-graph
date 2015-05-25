#!/usr/bin/env python

import dateutils


def quartiles(values):
    """
    Returns the (rough) quintlines of a series of values. This is not intended
    to be statistically correct - it's not a quick 'n' dirty measure.
    """
    return [i * max(values) / 4 for i in range(5)]


def longest_streak(dates):
    """
    Given a list of datetime.date objects, return the longest sublist of
    consecutive dates. If there are multiple longest sublists of the same
    length, then the first such sublist is returned.
    """
    if not dates:
        return []
    dates = sorted(dates)

    streaks = []
    current_streak = [dates[0]]

    # For each date, check to see whether it extends the current streak
    for idx in range(1, len(dates)):
        date = dates[idx]
        if dateutils.previous_day(date) == current_streak[-1]:
            current_streak.append(date)
        else:
            streaks.append(current_streak)
            current_streak = [date]

    # When we've gone through all the dates, save the last streak
    streaks.append(current_streak)

    return max(streaks, key=len)


def current_streak(dates):
    """
    Given a list of datetime.date objects, return today's date (if present)
    and all/any preceding consecutive dates.
    """
    streak = []
    current_date = dateutils.today()

    while current_date in dates:
        streak.append(current_date)
        current_date = dateutils.previous_day(current_date)

    return sorted(streak)