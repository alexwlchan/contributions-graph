#!/usr/bin/env python

import parser


class ContributionsGraph(object):

    def __init__(self, filepath, skip_weekends=False):
        self.filepath = filepath
        self.skip_weekends = skip_weekends
        self._parse_contributions_file()

    def _parse_contributions_file(self):
        """
        Parse the results and return a dict in which the
        keys are the dates, and the values are the contributions for that day.

        It expects each line of the file to be in the format

            YYYY-MM-DD value

        The returned dict only includes dates for the last year.
        """
        contributions = parser.parse_contributions_file(self.filepath,
                                                        self.skip_weekends)

        # Remove any dates with zero contributions from this dict: it means we
        # can use the keys as an indicator of days with non-zero contributions.
        for date, count in contributions.iteritems():
            if count == 0:
                del contributions[date]

        self.contributions = contributions

    def total_contributions(self):
        """
        Return the total number of contributions over the past year.
        """
        return sum(self.contributions.values())

    def longest_streak(self):
        """
        Returns the longest streak in the results.
        """
        return parser.longest_streak(self.contributions.keys(),
                                     self.skip_weekends)

    def current_streak(self):
        """
        Returns the current streak.
        """
        return parser.current_streak(self.contributions.keys(),
                                     self.skip_weekends)
