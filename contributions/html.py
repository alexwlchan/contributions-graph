#!/usr/bin/env python

from collections import namedtuple
import datetime

import dateutils

GridCell = namedtuple('GridCell', ['date', 'contributions'])


def _display_date(date):
    """
    Returns a long date string. Example output: "May 24, 2015".
    """
    return date.strftime("%B %d, %Y").replace(" 0", " ")


def cell_class(intervals):
    """
    Given a set of intervals, return a function which maps intervals to CSS
    classes denoting how notable a cell's contribution is. This is passed to
    the template to be used as a Jinja2 filter.
    """
    today = dateutils._today()
    start = datetime.date(today.year - 1, today.month, today.day)

    def cell_filter(cell):
        if not dateutils.is_within_last_year(cell.date):
            return "empty"
        elif cell.contributions == 0:
            return "none"
        elif cell.contributions <= intervals["low"]:
            return "low"
        elif cell.contributions <= intervals["med1"]:
            return "med1"
        elif cell.contributions <= intervals["med2"]:
            return "med2"
        else:
            return "high"

    return cell_filter


def grid_cells(contributions, skip_weekends):
    """
    The GitHub contributions graph is a grid of squares: one per date, with
    one row for each day of the month. This function takes a dict of
    contributions (date: int pairs), and returns a list of rows for this grid.
    Each row is a list of GridCell() instances.

    If skip_weekends is:
    * True, the result has seven rows, starting with Sunday
    * False, the result has five rows, starting with Monday
    """
    today = dateutils._today()
    start = datetime.date(today.year - 1, today.month, today.day)

    # If we're skipping weekends, then adjust the start and end dates so that
    # they both fall on weekdays.
    if skip_weekends:
        if not dateutils.is_weekday(today):
            today = dateutils.previous_day(today, skip_weekends)
        if not dateutils.is_weekday(start):
            start = dateutils.next_day(start, skip_weekends)

    # Create an empty list to populate with grid entries
    grid_entries = []

    # The first row is either a Sunday or a Monday (depending on whether we're
    # skipping weekends). Compute a list of dates for the first row.
    if skip_weekends:
        first_date = start - datetime.timedelta(start.weekday())
    else:
        first_date = start - datetime.timedelta(start.weekday() + 1 % 7)
    next_date = first_date

    first_row_dates = [first_date]
    while next_date <= today:
        next_date += datetime.timedelta(7)
        first_row_dates.append(next_date)

    # Now get contribution counts for each of these dates, and save the row
    first_row = [
        GridCell(date, contributions.get(date, 0)) for date in first_row_dates
    ]
    grid_entries.append(first_row)

    # For each subsequent day of the week, use this first row as a model: add
    # the appropriate number of days and get the count of contributions.
    if skip_weekends:
        weekdays = 5
    else:
        weekdays = 7

    for i in range(1, weekdays):
        row_dates = [day + datetime.timedelta(i) for day in first_row_dates]
        next_row = [
            GridCell(dd, contributions.get(dd, 0)) for dd in row_dates
        ]
        grid_entries.append(next_row)

    return grid_entries


def grid_template(contributions, skip_weekends):
    """
    Return a dict of variables to pass to the template for the basic grid.
    """
    grid_entries = grid_cells(contributions, skip_weekends)

    # Get the list of weekdays in the current locale
    weekdays = dateutils.weekday_initials()

    # Get the month at the top of each column
    months = [cell.date.strftime("%b") for cell in grid_entries[0]]

    variables = {
        "grid_entries": grid_entries,
        "weekdays": weekdays,
        "months": months
    }

    return variables


def filter_months(months):
    """
    We only want to print each month heading once, over the first column
    which contains days only from that month. This function filters a list of
    months so that only the first unique month heading is shown.
    """
    for idx in reversed(range(len(months))):
        if months[idx] == months[idx - 1]:
            months[idx] = ""

    # If the same month heading appears at the beginning and end of the year,
    # then only show it at the end of the year
    if months.count(months[0]) > 1:
        months[0] = ""
    if months.count(months[-1]) > 1:
        months[-1] = ""

    # Since each month takes up cells, we delete an empty space for each month
    # heading
    indices = [idx for idx, month in enumerate(months) if month]
    for idx in reversed(indices):
        del months[idx+1]

    return months


def filter_weekdays(skip_weekends):
    """
    We only want to print the M/W/F weekday labels, and we need to adjust the
    length of the weekdays in case we're skipping weekends.
    """
    weekdays = dateutils.weekday_initials()

    for idx in [0, 2, 4, 6]:
        weekdays[idx] = ""

    if skip_weekends:
        weekdays = weekdays[1:-1]

    return weekdays

