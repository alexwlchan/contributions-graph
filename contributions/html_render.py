#!/usr/bin/env python

def _display_date(date):
    """
    Returns a long date string. Example output: "May 24, 2015".
    """
    return date.strftime("%B %d, %Y").replace(" 0", " ")