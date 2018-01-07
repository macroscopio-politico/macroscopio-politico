#!/usr/bin/env python
import dash
from dash.dependencies import (
    Input,
    Output,
)
from flask import render_template

from polls.data import (
    years_to_show,
)
from server import server
from .layout import (
    layout,
    update,
)

dash_app = dash.Dash(__name__, sharing=True, server=server, url_base_pathname='/dash/polls/bubble')
dash_app.layout = layout

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
dash_app.config.suppress_callback_exceptions = True
scripts = dash_app._generate_scripts_html()
css = dash_app._generate_css_dist_html()
config = dash_app._generate_config_html()


@server.route('/polls/bubble')
def polls_bubble():
    return render_template('polls.html', css=css, js=scripts, config=config)

@dash_app.callback(
    Output('polls-chart', 'figure'),
    [
    Input('years-slider', 'value'),
    Input('x-axes-select', 'value'),
    Input('y-axes-select', 'value'),
    Input('bubble-size-select', 'value'),
    Input('grouping-select', 'value'),
    Input('regional-aggregation-select', 'value'),
    Input('political-aggregation-select', 'value')])
def polls_chart_change(
        year,
        x_axes,
        y_axes,
        bubble_size,
        grouping,
        regional_aggregation,
        political_aggregation):
    return update(
        str(year),
        x_axes=x_axes,
        y_axes=y_axes,
        bubble_size=bubble_size,
        grouping=grouping,
        regional_aggregation=regional_aggregation,
        political_aggregation=political_aggregation)


@dash_app.callback(
    Output('years-slider', 'min'),
    [Input('political-aggregation-select', 'value')])
def input_change(value):
    return years_to_show(value)[0]


@dash_app.callback(
    Output('years-slider', 'value'),
    [Input('political-aggregation-select', 'value')])
def input_change(value):
    return years_to_show(value)[0]


@dash_app.callback(
    Output('years-slider', 'max'),
    [Input('political-aggregation-select', 'value')])
def input_change(value):
    return years_to_show(value)[-1]


@dash_app.callback(
    Output('years-slider', 'marks'),
    [Input('political-aggregation-select', 'value')])
def input_change(value):
    return {i: '{}'.format(i) for i in years_to_show(value)}
