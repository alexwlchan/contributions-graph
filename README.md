# contribution-graph

This is a reimplementation of the Contributions chart from the GitHub user page, written in Python.



## Design

The main module presents an object, `ContributionGraph`, with two parameters for `__init__`:

*   `filename` -- string

    This contains a path to the file containing the contribution data (the format of which is tbc).

*   `include_weekends` -- boolean (default True)

    If you only want to track an item on weekdays (for example, if it was something you did on a weekday job, or at school), you can set this to False to exclude those days from the analysis.

It then presents the following methods:

*   `html()` -- render the analysis of the data in an HTML table, like on the GitHub page. Parameters:

    *   `color` -- the color scheme to use
    *   `title` -- the GitHub table is labelled "Contributions", but a different title may be appropriate
    *   `fullpage` -- boolean (default True). If this parameter is set to True, it returns a full HTML page. If not, it just returns the main block. Setting this to false means that you could get multiple tables and embed them in the same page.