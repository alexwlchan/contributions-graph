#!/usr/bin/env python

from collections import namedtuple
from datetime import date, timedelta

from jinja2 import Environment, PackageLoader

from dateutils import previous_day, next_day, is_weekday, weekday_initials

GridCell = namedtuple('GridCell', ['date', 'contributions'])


def cell_class(cell, intervals={"low": 5, "med1": 8, "med2": 12}):
    today = date.today()
    start = date(today.year - 1, today.month, today.day)
    if cell.date < start or cell.date > today:
        return "empty"
    if cell.contributions == 0:
        return "none"
    elif cell.contributions <= intervals["low"]:
        return "low"
    elif cell.contributions <= intervals["med1"]:
        return "med1"
    elif cell.contributions <= intervals["med2"]:
        return "med2"
    else:
        return "high"

env = Environment(loader=PackageLoader('contributions', 'templates'))
env.filters['cell_class'] = cell_class


def grid_template(contributions, skip_weekends):
    """
    Renders a grid.
    """
    today = date.today()
    start = date(today.year - 1, today.month, today.day)

    # If we're skipping weekends, then adjust the start and end dates so that
    # they both fall on weekdays.
    if skip_weekends:
        if not is_weekday(today):
            today = previous_day(today, skip_weekends)
        if not is_weekday(start):
            start = next_day(start, skip_weekends)

    # Create a list for populating with grid data
    grid_data = []

    # The first row is either a Sunday or a Monday (depending on whether we're
    # skipping weekends). Compute a list of dates for the first row.
    if skip_weekends:
        first_date = next_date = start - timedelta(start.weekday())
    else:
        first_date = next_date = start - timedelta(start.weekday() + 1 % 7)

    first_row_dates = [first_date]
    while next_date <= today:
        next_date += timedelta(7)
        first_row_dates.append(next_date)

    # Now we turn this list of dates into a set of GridCell objects, which
    # record the date, and the number of contributions on that date.
    first_row = [
        GridCell(dd, contributions.get(dd, 0)) for dd in first_row_dates
    ]
    grid_data.append(first_row)

    # For each subsequent day of the week, use this first row as a model: add
    # the appropriate number of days.
    if skip_weekends:
        weekdays = 5
    else:
        weekdays = 7

    for weekday in range(1, weekdays):
        row_dates = [day + timedelta(weekday) for day in first_row_dates]
        next_row = [
            GridCell(dd, contributions.get(dd, 0)) for dd in row_dates
        ]
        grid_data.append(next_row)

    # Now we create a list of month headings for the calendar. We mark the
    # first column in which every cell is part of that month.
    months = [d.strftime("%b") for d in first_row_dates]

    # Remove duplicates from the list
    for idx in reversed(range(len(months))):
        if months[idx] == months[idx - 1]:
            months[idx] = ""

    if months.count(months[0]) > 1:
        months[0] = ""

    # Get the list of weekdays in the current local
    weekdays = weekday_initials()

    # We only want to print the Monday, Wednesday, Friday rows, so clear out
    # the other weekdays
    for idx in [0, 2, 4, 6]:
        weekdays[idx] = ""

    if skip_weekends:
        weekdays = weekdays[1:-1]

    template = env.get_template("calendar.html")
    variables = {
        "grid_data": grid_data,
        "weekdays": weekdays,
        "months": months
    }

    return template, variables
