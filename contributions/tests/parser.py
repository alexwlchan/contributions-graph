#!/usr/bin/env python
"""
Unit tests for contributions.parser.
"""
from collections import defaultdict
import datetime
import logging
import os
import sys
import unittest

sys.path.append(os.getcwd())
from contributions import parser

logging.disable(logging.CRITICAL)


def _testfile(filename):
    return os.path.join(os.getcwd(), "contributions", "tests", filename)


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

    def test_parse_file(self):
        self.assertEqual(
            parser._parse_file(_testfile("file1.txt")),
            defaultdict(int)
        )

        self.assertEqual(
            parser._parse_file(_testfile("file2.txt")),
            defaultdict(int, {
                datetime.date(2012, 10, 9): 123,
                datetime.date(2012, 10, 8): 124
            })
        )

        self.assertEqual(
            parser._parse_file(_testfile("file3.txt")),
            defaultdict(int, {
                datetime.date(2012, 10, 9): 246,
                datetime.date(2012, 10, 8): 124
            })
        )


if __name__ == '__main__':
    unittest.main()
