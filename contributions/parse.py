#!/usr/bin/env python

import datetime

def within_last_year(date):
    """
    Returns True if a date falls within the last year, False otherwise.

    Takes a datetime object as an argument.
    """
    today = datetime.date.today()
    return datetime.datetime(today.year - 1, today.month, today.day) < date

def parse_contributions(file_path, date_format="%Y-%m-%d", separator=" "):
    """
    Given a path to a file, this function parses the file. It expects each line
    of the file to be in the format

        (date_fmt)(separator)(value)

    so an example line with the default settings would be

        2015-05-24 22

    Returns a dict in which the keys are the dates.
    """
    results = {}

    with open(file_path) as ff:
        for line in ff:
            date_str, value = line.strip().split(separator)

            try:
                date = datetime.datetime.strptime(date_str, date_format)
            except ValueError:
                print "Malformed date string in line:\n{}".format(line.strip())
                raise

            # Only add the result if the date is within the last year
            if within_last_year(date):
                results[date] = int(value)

    return results