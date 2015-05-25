#!/usr/bin/env python
"""
Unit tests for contributions.parser.
"""
import datetime
import logging
import os
import sys
import unittest

sys.path.append(os.getcwd())
from contributions import parser

logging.disable(logging.CRITICAL)


class TestParserMethods(unittest.TestCase):

    def test_parse_line(self):

        EMPTY_LINES = [
            "# this is a commented line",
            "   # this is a commented line with leading whitespace"
        ]
        for line in EMPTY_LINES:
            self.assertEqual(parser._parse_line(line), None)

        INVALID_LINES = [
            "too many spaces",
            "2015a-10-11 123",
            "2015-10-11 123a"
        ]
        for line in INVALID_LINES:
            with self.assertRaises(ValueError):
                parser._parse_line(line)

        VALID_LINES = {
            "2015-10-11 123": (datetime.date(2015, 10, 11), 123),
            "2016-11-9 18":   (datetime.date(2016, 11, 9), 18)
        }
        for line, output in VALID_LINES.iteritems():
            self.assertEqual(parser._parse_line(line), output)


if __name__ == '__main__':
    unittest.main()