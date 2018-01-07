# -*- coding: utf-8 -*-
import functools

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from candidates.data import (
    process_pie_data,
)
from candidates.menus import chart_menu
from common import (
    controls,
)
from .constants import (
    GROUPING_OPTIONS,
    POSITION_OPTIONS,
    VALUE_AXES_OPTIONS,
)

DEFAULT_CONFIG = dict(
    current_value_axes='Qtd. Votos',
    current_grouping='UF',
    current_political_aggregation='Presidente',
)

config = dict(**DEFAULT_CONFIG)


chart = dcc.Graph(
    id='candidates-chart', style={'margin': '20px 0px'},
)


def plot_figure(data):
    values_column = VALUE_AXES_OPTIONS[config['current_value_axes']]
    grouping_column = GROUPING_OPTIONS[config['current_grouping']]

    figure = dict(
        data=[],
        layout=go.Layout(
            title='{} por {}<br>para o cargo de {}'.format(
                config['current_value_axes'], config['current_grouping'],
                config['current_political_aggregation']
            ),
            margin={'l': 60, 'b': 40, 't': 110, 'r': 0},
            legend={'x': 0, 'y': 1},
    ),
    hoverinfo = 'label+percent+name',
    )

    plot_data = go.Pie(
        values=[],
        labels=[],
        name='',
    )

    for region_name in set(data.index):
        region_df = data.loc[[region_name]].reset_index()

        has_text_value = grouping_column in region_df.columns

        for _, row in region_df.iterrows():
            plot_data['values'].append(row[values_column])
            plot_data['labels'].append(
                '{}'.format(
                    str(row[grouping_column] if has_text_value else region_name)
                )
            )

        figure['data'].append(plot_data)

    return figure


@functools.lru_cache()
def update(value_axes=None, grouping=None, political_aggregation=None):
    if value_axes is None:
        value_axes = config['current_value_axes']

    if grouping is None:
        grouping = config['current_grouping']

    if political_aggregation is None:
        political_aggregation = config['current_political_aggregation']

    votos_df, years = process_pie_data(
        value_column=VALUE_AXES_OPTIONS[value_axes],
        grouping_column=GROUPING_OPTIONS[grouping],
        position=POSITION_OPTIONS[political_aggregation])

    data = votos_df

    config['current_value_axes'] = value_axes
    config['current_grouping'] = grouping
    config['current_political_aggregation'] = political_aggregation

    return plot_figure(data)


value_axes_select = controls.value_axes_select(
    value=config['current_value_axes'], options=VALUE_AXES_OPTIONS)
grouping_select = controls.grouping_select(
    value=config['current_grouping'], options=GROUPING_OPTIONS)
political_aggregation_select = controls.political_aggregation_select(
    value=config['current_political_aggregation'], options=POSITION_OPTIONS)


layout = html.Div(className='chart-container', children=[
    html.Div(className='container', children=[
        chart_menu(),
        html.Div(className='row', children=[
            value_axes_select, grouping_select, political_aggregation_select
        ]),
        html.Div(className='container-fluid', children=[
            chart
        ]),
    ])
])
