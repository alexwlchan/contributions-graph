#!/usr/bin/env python
"""
Unit tests for contributions.parser.
"""

from datetime import date
import os
import sys
import unittest

import mock

sys.path.append(os.getcwd())
from contributions import dateutils, parser


dateutils._today = mock.Mock()
dateutils._today.return_value = date(2015, 4, 24)


def _testdate(day):
    return date(2015, 4, day)

def _testrange(days):
    return [_testdate(day) for day in days]

def _test_long(days, skip_weekends):
    return parser.longest_streak(_testrange(days), skip_weekends)

def _test_curr(days, skip_weekends):
    return parser.current_streak(_testrange(days), skip_weekends)


class TestParserMethods(unittest.TestCase):

    def test_longest_streak(self):
        # Note that 19, 25 and 26 are weekend days. We expect this test case
        # just to pick out the longest streak:
        self.assertEqual(
            _test_long([19, 20, 21, 25, 26, 27, 28], False),
            _testrange([25, 26, 27, 28])
        )

        # But this test case should ignore 19, 25 and 26:
        self.assertEqual(
            _test_long([19, 20, 21, 22, 25, 26, 27, 28], True),
            _testrange([20, 21, 22])
        )

        # Check that changing the order doesn't affect the result
        self.assertEqual(
            _test_long([19, 20, 21, 25, 26, 22, 23], False),
            _testrange([19, 20, 21, 22, 23])
        )
        self.assertEqual(
            _test_long([19, 20, 21, 25, 26, 22, 23], True),
            _testrange([20, 21, 22, 23])
        )

        # Check what happens when the test case runs over a weekend
        self.assertEqual(
            _test_long([3, 4, 5, 6, 7, 8], True),
            _testrange([6, 7, 8])
        )
        self.assertEqual(
            _test_long([3, 4, 5, 6, 7, 8], False),
            _testrange([3, 4, 5, 6, 7, 8])
        )


    def test_current_streak(self):
        # First, we have a streak in which we don't include "today's" date, so
        # the current streak should be empty.
        self.assertEqual(
            _test_curr([3, 4, 5, 6, 7, 8], False),
            []
        )
        self.assertEqual(
            _test_curr([3, 4, 5, 6, 7, 8], True),
            []
        )

        # Now a current streak which stops midway through a weekend
        self.assertEqual(
            _test_curr([19, 20, 21, 22, 23, 24], False),
            _testrange([19, 20, 21, 22, 23, 24])
        )
        self.assertEqual(
            _test_curr([19, 20, 21, 22, 23, 24], True),
            _testrange([20, 21, 22, 23, 24])
        )

        # Now a current streak which goes over a weekend boundary
        self.assertEqual(
            _test_curr([17, 18, 19, 20, 21, 22, 23, 24], False),
            _testrange([17, 18, 19, 20, 21, 22, 23, 24])
        )
        self.assertEqual(
            _test_curr([17, 18, 19, 20, 21, 22, 23, 24], True),
            _testrange([17, 20, 21, 22, 23, 24])
        )



if __name__ == '__main__':
    unittest.main()
