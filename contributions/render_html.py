#!/usr/bin/env python
"""
The 'templates' directory contains two Jinja2 templates for rendering the
graph:

* `index.html` - the skeleton which only loads the CSS files, and then includes
  the output of the second template:
* `graph.html` - this is the template which actually renders a graph.

This module is responsible for preparing and rendering the templates.
"""

from collections import namedtuple
import datetime
from types import StringTypes
import ntpath

from jinja2 import Environment, PackageLoader

import contributions.dateutils as dateutils
import contributions.parser as parser
import contributions.statistics as statistics

GridCell = namedtuple('GridCell', ['date', 'contributions'])


def create_graph(filepaths):
    """
    Prepare the `index.html` template.
    """
    graphs = []
    if isinstance(filepaths, StringTypes):
        filepaths = [filepaths]

    for path in filepaths:
        contributions = parser.parse_file(path)

        graph = {
            "data": gridify_contributions(contributions),
            "cell_class": _cell_class(contributions.values()),
            "longest_streak": statistics.longest_streak(
                [key for key, val in contributions.iteritems() if val > 0]
            ),
            "current_streak": statistics.current_streak(
                [key for key, val in contributions.iteritems() if val > 0]
            ),
            "sum": sum(contributions.itervalues()),
            "repo_name": ntpath.basename(path)
        }

        graph["last_date"] = (
            [""] + sorted([key for key, v in contributions.iteritems() if v])
        )[-1]

        graphs.append(graph)

    env = Environment(loader=PackageLoader('contributions', 'templates'))

    env.filters['tooltip'] = tooltip_text
    env.filters['display_date'] = dateutils.display_date
    env.filters['elapsed_time'] = dateutils.elapsed_time

    template = env.get_template("index.html")

    weekdays = dateutils.weekday_initials()
    for idx in [0, 2, 4, 6]:
        weekdays[idx] = ""

    months = [
        cell.date.strftime("%b")
        for cell in gridify_contributions(contributions)[0]
    ]
    months = filter_months(months)

    return template.render(graphs=graphs,
                           today=dateutils.today(),
                           start=dateutils.start(),
                           weekdays=weekdays,
                           months=months)


def gridify_contributions(contributions):
    """
    The contributions graph has seven rows (one for each day of the week).
    It spans a year. Given a dict of date/value pairs, rearrange these results
    into seven rows of "cells", where each cell records a date and a value.
    """
    start = dateutils.start()
    today = dateutils.today()

    graph_entries = []

    # The first row is a Sunday, so go back to the last Sunday before the start
    if start.weekday() == 6:
        first_date = start
    else:
        first_date = start - datetime.timedelta(start.weekday() + 1 % 7)
    next_date = first_date

    first_row_dates = [first_date]
    while (next_date <= today) and (next_date + datetime.timedelta(7) <= today):
        next_date += datetime.timedelta(7)
        first_row_dates.append(next_date)

    # Now get contribution counts for each of these dates, and save the row
    first_row = [
        GridCell(date, contributions[date]) for date in first_row_dates
    ]
    graph_entries.append(first_row)

    # For each subsequent day of the week, use the first row as a model: add
    # the appropriate number of days and count the contributions
    for i in range(1, 7):
        row_dates = [day + datetime.timedelta(i) for day in first_row_dates]
        next_row = [
            GridCell(date, contributions[date]) for date in row_dates
        ]
        graph_entries.append(next_row)

    return graph_entries


def tooltip_text(cell):
    """
    Returns the tooltip text for a cell.
    """
    if cell.contributions == 0:
        count = "No contributions"
    elif cell.contributions == 1:
        count = "1 contribution"
    else:
        count = "%d contributions" % cell.contributions
    date_str = dateutils.display_date(cell.date)
    return "<strong>%s</strong> on %s" % (count, date_str)


def _cell_class(values):
    """
    Returns a function which determines how a cell is highlighted.
    """
    quartiles = statistics.quartiles(values)
    def class_label(cell):
        if cell.date > dateutils.today() or cell.date < dateutils.start():
            return "empty"
        elif cell.contributions == 0:
            return "grad0"
        elif cell.contributions <= quartiles[1]:
            return "grad1"
        elif cell.contributions <= quartiles[2]:
            return "grad2"
        elif cell.contributions <= quartiles[3]:
            return "grad3"
        else:
            return "grad4"
    return class_label


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
        if idx != len(months) - 1:
            del months[idx+1]

    return months
