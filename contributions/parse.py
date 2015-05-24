#!/usr/bin/env python

from collections import defaultdict
import datetime


def within_last_year(date):
    """
    Returns True if a date falls within the last year, False otherwise.

    Takes a datetime.date as an argument.
    """
    today = datetime.date.today()
    return datetime.date(today.year - 1, today.month, today.day) < date


def parse_contributions(file_path):
    """
    Given a path to a file, this function parses the file. It expects each line
    of the file to be in the format

        %Y-%m-%d $value

    Returns a dict in which the keys are the dates.
    """
    results = defaultdict(int)

    with open(file_path) as ff:
        for line in ff:

            # Skip empty lines
            if not line.strip():
                continue

            date_str, value = line.strip().split(" ")

            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print "Malformed date string in line:\n{}".format(line.strip())
                raise

            # Only add the result if the date is within the last year
            if within_last_year(date):
                results[date] += int(value)

    return results


def total_contributions(results):
    """
    Given a results dictionary, this returns the total number of contributions
    in the last year.
    """
    return sum(results.itervalues())


def longest_streak(results):
    """
    Returns the longest streak in the results. Assumes that results is
    non-empty.
    """
    # First, we turn the list of dates into integers counting the number of
    # days since 1 year ago.
    today = datetime.date.today()
    start = datetime.date(today.year - 1, today.month, today.day)

    days = sorted((day - start).days for day in results.keys()
                                         if results[day] > 0)

    # To find the longest streak, we split the list 'days' into runs of
    # consecutive integers.
    streaks = []
    current_streak = [days[0]]

    # Go through each day in the list. If it's one after the last day in
    # 'current', then append it to that streak and carry on. If not, save the
    # current streak and start a new one.
    for idx in range(1, len(days)):
        if days[idx] == current_streak[-1] + 1:
            current_streak.append(days[idx])
        else:
            streaks.append(current_streak)
            current_streak = [days[idx]]

    # When we've run out of days, append the last streak.
    streaks.append(current_streak)

    # Get the longest streak. Because the list is sorted in ascending order,
    # if there are multiple longest streaks of the same length, it gets the
    # first such streak.
    longest_streak = max(streaks, key=len)

    # Turn the list back into a series of dates
    return [start + datetime.timedelta(day) for day in longest_streak]


def current_streak(results):
    """
    Returns the length of the current streak in the results.
    """
    today = start = datetime.date.today()
    streak_length = 0

    while start in results.keys():
        start -= datetime.timedelta(1)
        streak_length += 1

    return streak_length
