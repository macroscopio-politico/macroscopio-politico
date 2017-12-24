# -*- coding: utf-8 -*-
import functools

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from common import (
    controls,
)
from polls.data import (
    process_bar_data,
)
from polls.menus import chart_menu
from .constants import (
    GROUPING_OPTIONS,
    POSITION_OPTIONS,
    X_AXES_OPTIONS,
    Y_AXES_OPTIONS,
)

DEFAULT_CONFIG = dict(
    current_x_axes='Ano',
    current_y_axes='Qtd. Comparecimento',
    current_grouping='Brasil',
    current_political_aggregation='Presidente',
)

config = dict(**DEFAULT_CONFIG)


chart = dcc.Graph(
    id='polls-chart', style={'margin': '20px 0px'},
)


def plot_figure(data):
    x_column = X_AXES_OPTIONS[config['current_x_axes']]
    y_column = Y_AXES_OPTIONS[config['current_y_axes']]
    grouping_column = GROUPING_OPTIONS[config['current_grouping']]

    figure = dict(
        data=[],
        layout=go.Layout(
            title='{} x {}<br>por {}<br>para o cargo de {}'.format(
                config['current_x_axes'], config['current_y_axes'], config['current_grouping'],
                config['current_political_aggregation']
            ),
            xaxis={'type': 'log', 'title': config['current_x_axes']},
            yaxis={'title': config['current_y_axes']},
            margin={'l': 60, 'b': 40, 't': 110, 'r': 0},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )

    for region_name in set(data.index):
        region_df = data.loc[region_name].reset_index()

        plot_data = go.Bar(
            x=[],
            y=[],
            text=[],
            name=region_name
        )

        has_text_value = grouping_column in region_df.columns

        for _, row in region_df.iterrows():
            plot_data['x'].append(row[x_column])
            plot_data['y'].append(row[y_column])
            plot_data['text'].append(
                '{}'.format(
                    str(row[grouping_column] if has_text_value else region_name)
                )
            )

        figure['data'].append(plot_data)

    return figure


@functools.lru_cache()
def update(x_axes=None, y_axes=None, grouping=None, political_aggregation=None):
    if x_axes is None:
        x_axes = config['current_x_axes']

    if y_axes is None:
        y_axes = config['current_y_axes']

    if grouping is None:
        grouping = config['current_grouping']

    if political_aggregation is None:
        political_aggregation = config['current_political_aggregation']

    votos_df, years = process_bar_data(
        x_column=X_AXES_OPTIONS[x_axes],
        y_column=Y_AXES_OPTIONS[y_axes],
        grouping_column=GROUPING_OPTIONS[grouping],
        position=POSITION_OPTIONS[political_aggregation])

    data = votos_df

    config['current_x_axes'] = x_axes
    config['current_y_axes'] = y_axes
    config['current_grouping'] = grouping
    config['current_political_aggregation'] = political_aggregation

    return plot_figure(data)


x_axes_select = controls.x_axes_select(value=config['current_x_axes'], options=X_AXES_OPTIONS)
y_axes_select = controls.y_axes_select(value=config['current_y_axes'], options=Y_AXES_OPTIONS)


grouping_select = controls.grouping_select(
    value=config['current_grouping'], options=GROUPING_OPTIONS)
political_aggregation_select = controls.political_aggregation_select(
    value=config['current_political_aggregation'], options=POSITION_OPTIONS)


layout = html.Div(className='chart-container', children=[
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=True),
    html.Div(className='container', children=[
        chart_menu(),
        html.Div(className='row', children=[
            x_axes_select, y_axes_select
        ]),
        html.Div(className='row', children=[
            grouping_select, political_aggregation_select
        ]),
        html.Div(className='container-fluid', children=[
            chart
        ]),
    ])
])
