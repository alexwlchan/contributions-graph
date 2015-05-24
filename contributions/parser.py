#!/usr/bin/env python

import dateutils


def longest_streak(dates, skip_weekends):
    """
    Given a list of datetime.date objects, return the longest sublist of
    consecutive dates. If there are multiple longest sublists of the same
    length, then the first such sublist is returned.

    If skip_weekends is set to True, then a Friday and the following Monday
    are regarded as consecutive.
    """
    if not dates:
        return []
    dates = sorted(dates)

    streaks = []
    current_streak = [dates[0]]

    # For each date, check to see whether it extends the current streak
    for idx in range(1, len(dates)):
        date = dates[idx]
        if dateutils.previous_day(date, skip_weekends) == current_streak[-1]:
            current_streak.append(date)
        else:
            streaks.append(current_streak)
            current_streak = [date]

    # When we've gone through all the dates, save the last streak
    streaks.append(current_streak)

    # Get the longest streak. Because we sorted the list at the start, if there
    # are multiple longest streaks, we get the first one. It's a nice
    # coincidence that this matches the way GitHub's contributions graph works.
    return max(streaks, key=len)


def current_streak(dates, skip_weekends):
    """
    Given a list of datetime.date objects, return today's date (if present)
    and all/any preceding consecutive dates.
    """
    streak = []
    current_date = dateutils._today()

    while current_date in dates:
        streak.append(current_date)
        current_date = dateutils.previous_day(current_date, skip_weekends)

    return sorted(streak)