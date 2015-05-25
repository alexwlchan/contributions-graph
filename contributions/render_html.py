#!/usr/bin/env python
"""
The 'templates' directory contains two Jinja2 templates for rendering the
graph:

* `index.html` - the skeleton which only loads the CSS files, and then includes
  the output of the second template:
* `graph.html` - this is the template which actually renders a graph.

This module is responsible for preparing and rendering the templates.
"""

from jinja2 import Environment, PackageLoader

def _prepare_template():
    """
    Prepare the `index.html` template.
    """
    env = Environment(loader=PackageLoader('contributions', 'templates'))

    template = env.get_template("index.html")

    return template

def render_template(graphs):
    """
    Render the `index.html` template with the given graphs.
    """
    template = _prepare_template()
    return template.render(graphs=graphs)