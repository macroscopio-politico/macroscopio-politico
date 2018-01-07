#!/usr/bin/env python
import dash
from dash.dependencies import (
    Input,
    Output,
)
from flask import render_template

from server import server
from .layout import (
    layout,
    update,
)

dash_app = dash.Dash(__name__, sharing=True, server=server, url_base_pathname='/dash/candidates/line')
dash_app.layout = layout

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
dash_app.config.suppress_callback_exceptions = True
scripts = dash_app._generate_scripts_html()
css = dash_app._generate_css_dist_html()
config = dash_app._generate_config_html()


@server.route('/candidates/line')
def candidates_line():
    return render_template('candidates.html', css=css, js=scripts, config=config)

@dash_app.callback(
    Output('candidates-chart', 'figure'),
    [
    Input('x-axes-select', 'value'),
    Input('y-axes-select', 'value'),
    Input('grouping-select', 'value'),
    Input('political-aggregation-select', 'value')])
def candidates_chart_change(
        x_axes,
        y_axes,
        grouping,
        political_aggregation):
    return update(
        x_axes=x_axes,
        y_axes=y_axes,
        grouping=grouping,
        political_aggregation=political_aggregation)
