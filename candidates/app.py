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
    years_to_show,
)

dash_app = dash.Dash(__name__, sharing=True, server=server, url_base_pathname='/dash/candidates')
dash_app.layout = layout

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
dash_app.config.suppress_callback_exceptions = True
scripts = dash_app._generate_scripts_html()
css = dash_app._generate_css_dist_html()
config = dash_app._generate_config_html()


@server.route('/candidates')
def candidates():
    return render_template('candidates.html', css=css, js=scripts, config=config)


@dash_app.callback(
    Output('candidates-chart', 'figure'),
    [Input('years-slider', 'value'),
    Input('x-axes-select', 'value'),
    Input('y-axes-select', 'value'),
    Input('bubble-size-select', 'value'),
    Input('bubble-color-select', 'value'),
    Input('political-aggregation-select', 'value')])
def candidates_chart_change(year, x_axes, y_axes, bubble_size, bubble_color, political_aggregation):
    return update(str(year), x_axes=x_axes, y_axes=y_axes, bubble_size=bubble_size,
                  bubble_color=bubble_color, political_aggregation=political_aggregation)


@dash_app.callback(
    Output('years-slider', 'min'),
    [Input('political-aggregation-select', 'value')])
def skider_min_change(value):
    return years_to_show(value)[0]


@dash_app.callback(
    Output('years-slider', 'value'),
    [Input('political-aggregation-select', 'value')])
def skider_min_change(value):
    return years_to_show(value)[0]


@dash_app.callback(
    Output('years-slider', 'max'),
    [Input('political-aggregation-select', 'value')])
def skider_min_change(value):
    return years_to_show(value)[-1]


@dash_app.callback(
    Output('years-slider', 'marks'),
    [Input('political-aggregation-select', 'value')])
def skider_min_change(value):
    return {i: '{}'.format(i) for i in years_to_show(value)}
