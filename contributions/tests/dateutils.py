#!/usr/bin/env python
"""
Unit tests for contributions.dateutils.
"""

from datetime import date
import locale
import os
import sys
import unittest

import mock

sys.path.append(os.getcwd())
from contributions import dateutils


dateutils._today = mock.Mock()
dateutils._today.return_value = date(2015, 4, 24)


INCREMENT_CASES = [
    [date(2015, 5, 29), date(2015, 5, 28), False],
    [date(2015, 5, 25), date(2015, 5, 24), False],
    [date(2015, 5, 25), date(2015, 5, 22), True],
]

WEEKDAY_NAMES = {
    'en_US': ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su'],
    'de_DE': ['Mo', 'Di', 'Mi', 'Do', 'F', 'Sa', 'So'],
    'fr_FR': ['L', 'Ma', 'Me', 'J', 'V', 'S', 'D']
}

PAST_DATE_STRINGS = {
    date(2015, 4, 23): "a day ago",
    date(2015, 4, 21): "3 days ago",
    date(2015, 3, 26): "29 days ago",
    date(2015, 3, 25): "a month ago",
    date(2014, 8, 25): "8 months ago",
    date(2014, 4, 24): "12 months ago",
    date(2014, 4, 23): "more than a year ago",
}


class TestDateutilMethods(unittest.TestCase):

    def test_weekday(self):
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 3)), False)
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 4)), True)
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 5)), True)
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 6)), True)
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 7)), True)
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 8)), True)
        self.assertEqual(dateutils.is_weekday(date(2015, 5, 9)), False)

    def test_is_within_last_year(self):
        self.assertEqual(
            dateutils.is_within_last_year(date(2008, 10, 8)), False)
        self.assertEqual(
            dateutils.is_within_last_year(date(2006, 10, 8)), False)
        self.assertEqual(
            dateutils.is_within_last_year(date(2015, 4, 21)), True)

        # We count the same date on the previous year as "within one year", but
        # not the day before that
        self.assertEqual(
            dateutils.is_within_last_year(date(2014, 4, 23)), False)
        self.assertEqual(
            dateutils.is_within_last_year(date(2014, 4, 24)), True)

        # Future dates aren't within the past year
        self.assertEqual(
            dateutils.is_within_last_year(date(2016, 8, 21)), False)

    def test_previous_day(self):
        for date1, date2, skip in INCREMENT_CASES:
            self.assertEqual(dateutils.previous_day(date1, skip), date2)

    def test_next_day(self):
        for date2, date1, skip in INCREMENT_CASES:
            self.assertEqual(dateutils.next_day(date1, skip), date2)

    def test_weekday_initials(self):
        for locale_code, weekdays in WEEKDAY_NAMES.iteritems():
            locale.setlocale(locale.LC_ALL, locale_code)
            self.assertEqual(dateutils.weekday_initials(), weekdays)

    def test_past_date_str(self):
        for date_obj, date_str in PAST_DATE_STRINGS.iteritems():
            self.assertEqual(dateutils.past_date_str(date_obj), date_str)

if __name__ == '__main__':
    unittest.main()
