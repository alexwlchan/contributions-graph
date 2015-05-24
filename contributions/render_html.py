#!/usr/bin/env python

from collections import namedtuple
from datetime import date, timedelta

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('contributions', 'templates'))

GridCell = namedtuple('GridCell', ['date', 'contributions'])

today = date.today()
start = date(today.year - 1, today.month, today.day)

data = []

# The first row in the calendar is a Sunday, which is 6 by the weekday()
# method. Compute a list of dates for the first row, and store them as
# (Y, M, D) tuples.
date1 = start - timedelta(start.weekday() + 1 % 7)
sundays = []
sundays.append(date1)

while date1 <= today:
    date1 += timedelta(7)
    sundays.append(date1)


data.append(GridCell(date, 0) for date in sundays)

# For each subsequent day, use Sunday as a model: take the corresponding day
# of that week and add the appropriate number of days
for i in range(1, 7):
    newrow = [
        day + timedelta(i) for day in sundays
    ]
    data.append(GridCell(date, 0) for date in newrow)

months = [d.strftime("%b") for d in sundays]
for idx in reversed(range(len(months))):
    if months[idx] == months[idx - 1]:
        months[idx] = ""
months[0] = ""
indices = [idx for idx, month in enumerate(months) if month]
for i in reversed(indices):
    del months[i+1]

weekdays = ['', 'M', '', 'W', '', 'F', '']

def cell_class(cell):
    """
    """
    intervals = {"low": 5, "med1": 8, "med2": 12}
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

env.filters['cell_class'] = cell_class

template = env.get_template("calendar.html")

print template.render(data=[list(x) for x in data], weekdays=weekdays, months=months)