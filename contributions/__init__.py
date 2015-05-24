#!/usr/bin/env python

from collections import defaultdict
from datetime import date, datetime, timedelta

from dateutils import is_weekday, previous_day
from render_html import grid_template


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
        contributions = defaultdict(int)

        with open(self.filepath) as ff:
            for line in ff:

                # Skip blank lines
                if not line.strip(): continue

                date_str, value = line.strip().split(" ")
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    print "Malformed date in this line:\n%s" % line.strip()
                    raise

                # Only add the line if the date is within the last year.
                if _is_within_last_year(date):
                    # If skip_weekends is True, only include the value if this
                    # is a weekday.
                    if self.skip_weekends and not is_weekday(date):
                        continue
                    contributions[date] += int(value.strip())

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
        # If there are no contributions, then there can't be any streak.
        if not self.contributions:
            return []
        else:
            days = sorted(self.contributions.keys())

            streaks = []
            current_streak = [days[0]]

            # Go through each day in the list. If it comes after the latest day
            # in the current streak, then it's part of the same streak. If not,
            # then it's part of a new streak.
            for idx in range(1, len(days)):
                if previous_day(days[idx], self.skip_weekends) == current_streak[-1]:
                    current_streak.append(days[idx])
                else:
                    streaks.append(current_streak)
                    current_streak = [days[idx]]

            # When we've run out of days, save the last streak.
            streaks.append(current_streak)

            # Get the longest streak. Because of the way the list of sorted, if
            # there are multiple longest streaks of the same length, it gets
            # the first such streak.
            return max(streaks, key=len)

    def current_streak(self):
        """
        Returns the current streak.
        """
        today = current_date = date.today()
        streak = []

        while current_date in self.contributions.keys():
            streak.append(current_date)
            current_date = _previous_day(current_date, self.skip_weekends)

        return streak

    def render_grid(self):
        template, variables = grid_template(self.contributions,
                                            self.skip_weekends)
        variables["total_contributions"] = self.total_contributions()
        today = date.today()
        variables["today"] = _display_date(today)
        variables["start"] = _display_date(date(today.year - 1,
                                                today.month,
                                                today.day))

        longest = self.longest_streak()
        variables["longest_start"] = _display_date(longest[0])
        variables["longest_end"] = _display_date(longest[1])
        variables["longest_length"] = len(longest)

        print template.render(**variables)

