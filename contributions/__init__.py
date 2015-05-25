#!/usr/bin/env python

from jinja2 import Environment, PackageLoader

import parser
import html


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

    def refresh(self):
        self._parse_contributions_file()

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

    def render_html(self,
                    intervals=None,
                    color_scheme="green",
                    title="Contributions",
                    fullpage=True):
        """
        Render the contributions graph in HTML.

        :param intervals: This should be a dict with three keys: low, med1 and
                          med2. These denote the degrees of achievement.
        :param color_scheme: One of "red", "green" or "blue"
        :param title: The title to display at the top of the graph
        :param fullpage If set to True, return a full HTML page. If not, return
                        just the grid part.
        """
        env = Environment(loader=PackageLoader('contributions', 'templates'),
                          trim_blocks=True)

        env.filters['cell_class'] = html.cell_class(intervals)

        variables = html.grid_template(self.contributions,
                                              self.skip_weekends)

        template = env.get_template("calendar.html")

        variables["months"] = html.filter_months(variables["months"])
        variables["weekdays"] = html.filter_weekdays(self.skip_weekends)
        variables["title"] = title

        return template.render(**variables)















