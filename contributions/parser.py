#!/usr/bin/env python
"""
The record of contributions is in a text file, where each line is in the
following format:

    YYYY-MM-DD value

Excess whitespace is not significant, and text after a hash (#) will be treated
as a comment. Blank lines are skipped.

This module is responsible for parsing the output of this file, and turning it
into a dictionary of date/contribution count pairs.
"""

from collections import defaultdict
import datetime
import logging


def _parse_line(original_line):
    """
    Parse the output of a single line from the file. Returns a (date, count)
    tuple if the line contains content, or None if the line contains no
    content.
    """
    # Remove any comments and excess whitespace from the line
    line = original_line.split("#")[0].strip()

    # If the line is empty, then there's nothing more to do
    if not line:
        return

    # Split the string into a date string, and a value
    try:
        date_str, count_str = line.split()

        # Try to coerce the date string into a datetime.date object:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            logging.warning("Invalid date in line:{}".format(original_line))
            raise

        # Try to coerce the count into an int
        try:
            count = int(count_str)
        except ValueError:
            logging.warning("Invalid count in line: {}".format(original_line))
            raise

    # If the line has too many or too few values separated by spaces, then a
    # ValueError will be raised.
    except ValueError:
        logging.warning("Invalid line:{}".format(original_line))
        raise

    return (date, count)


def parse_file(filepath):
    """
    Parse the output of a file containing contribution data. Returns a dict of
    date/count pairs.
    """
    contributions = defaultdict(int)

    with open(filepath) as f:
        for line in f:
            line_output = _parse_line(line)
            if line_output is not None:
                date, count = line_output
                contributions[date] += count
    return contributions

