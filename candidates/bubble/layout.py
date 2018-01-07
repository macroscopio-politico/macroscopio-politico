# -*- coding: utf-8 -*-
import functools

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from candidates.data import (
    process_data,
    years_to_show,
)
from candidates.menus import chart_menu
from common import (
    controls,
)
from .constants import (
    BUBBLE_SIZE_OPTIONS,
    GROUPING_OPTIONS,
    POSITION_OPTIONS,
    REGION_OPTIONS,
    X_AXES_OPTIONS,
    Y_AXES_OPTIONS,
)

DEFAULT_CONFIG = dict(
    current_x_axes='Média da Qtd. Votos',
    current_y_axes='Desvio Padrão da Qtd. Votos',
    current_bubble_size='Qtd. Candidatos',
    current_grouping='Gênero',
    current_regional_aggregation='Macrorregião',
    current_political_aggregation='Presidente',
)

config = dict(**DEFAULT_CONFIG)


chart = dcc.Graph(
    id='candidates-chart', style={'margin': '20px 0px'},
)


def plot_figure(data):
    x_column = X_AXES_OPTIONS[config['current_x_axes']]
    y_column = Y_AXES_OPTIONS[config['current_y_axes']]
    bubble_size_column = BUBBLE_SIZE_OPTIONS[config['current_bubble_size']]
    grouping_column = GROUPING_OPTIONS[config['current_grouping']]

    figure = dict(
        data=[],
        layout=go.Layout(
            title='{} x {}<br>por {}<br>para o cargo de {} no ano de {}'.format(
                config['current_x_axes'], config['current_y_axes'], config['current_grouping'],
                config['current_political_aggregation'], config['current_year']
            ),
            xaxis={'type': 'log', 'title': config['current_x_axes']},
            yaxis={'title': config['current_y_axes']},
            margin={'l': 60, 'b': 40, 't': 110, 'r': 0},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )

    default_size_ref = 2 * data.loc[:, bubble_size_column].max() / (100**2)

    for region_name in set(data.index):
        region_df = data.loc[[region_name]]

        plot_data = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            opacity=0.7,
            marker={
                'sizemode': 'area',
                'sizeref': default_size_ref,
                'sizemin': 5,
                'opacity': 0.7,
                'size': [],
            },
            name=region_name
        )

        has_text_value = grouping_column in region_df.columns

        for _, row in region_df.iterrows():
            plot_data['x'].append(row[x_column])
            plot_data['y'].append(row[y_column])
            plot_data['text'].append(
                '{}<br>Turno: {}º<br>{}: {} ({:.2%})'.format(
                    str(row[grouping_column] if has_text_value else region_name),
                    str(row['NUM_TURNO']),
                    config['current_bubble_size'],
                    str(row[bubble_size_column]),
                    float(row['TEXT_PERCENTAGE']),
                )
            )
            plot_data['marker']['size'].append(row[bubble_size_column])

        figure['data'].append(plot_data)

    return figure


@functools.lru_cache()
def update(current_year=None, x_axes=None, y_axes=None, bubble_size=None,
           grouping=None, regional_aggregation=None, political_aggregation=None):
    if x_axes is None:
        x_axes = config['current_x_axes']

    if y_axes is None:
        y_axes = config['current_y_axes']

    if bubble_size is None:
        bubble_size = config['current_bubble_size']

    if grouping is None:
        grouping = config['current_grouping']

    if regional_aggregation is None:
        regional_aggregation = config['current_regional_aggregation']

    if political_aggregation is None:
        political_aggregation = config['current_political_aggregation']

    votos_df, years = process_data(
        bubble_size_column=BUBBLE_SIZE_OPTIONS[bubble_size],
        grouping_column=GROUPING_OPTIONS[grouping],
        regional_aggregation_column=REGION_OPTIONS[regional_aggregation],
        position=POSITION_OPTIONS[political_aggregation])

    if current_year is None:
        current_year = years[0]

    if int(current_year) < int(years[0]):
        current_year = years[0]

    data = votos_df.loc[str(current_year)]

    config['current_year'] = current_year
    config['current_x_axes'] = x_axes
    config['current_y_axes'] = y_axes
    config['current_bubble_size'] = bubble_size
    config['current_grouping'] = grouping
    config['current_regional_aggregation'] = regional_aggregation
    config['current_political_aggregation'] = political_aggregation

    return plot_figure(data)


x_axes_select = controls.x_axes_select(
    value=config['current_x_axes'], options=X_AXES_OPTIONS)
y_axes_select = controls.y_axes_select(
    value=config['current_y_axes'], options=Y_AXES_OPTIONS)
bubble_size_select = controls.bubble_size_select(
    value=config['current_bubble_size'], options=BUBBLE_SIZE_OPTIONS)
grouping_select = controls.grouping_select(
    value=config['current_grouping'], options=GROUPING_OPTIONS)
regional_aggregation_select = controls.regional_aggregation_select(
    value=config['current_regional_aggregation'], options=REGION_OPTIONS)
political_aggregation_select = controls.political_aggregation_select(
    value=config['current_political_aggregation'], options=POSITION_OPTIONS)


play_row = html.Div(className='row', children=[
    html.Div(className='col-12', style={'margin': '25px 0px'}, children=[
        dcc.Slider(
            min=years_to_show(config['current_political_aggregation'])[0],
            max=years_to_show(config['current_political_aggregation'])[-1],
            marks={i: '{}'.format(i) for i in years_to_show(config['current_political_aggregation'])},
            value=years_to_show(config['current_political_aggregation'])[0],
            step=4,
            dots=True,
            updatemode='drag',
            id='years-slider'
        )
    ]),
])


layout = html.Div(className='chart-container', children=[
    html.Div(className='container', children=[
        chart_menu(),
        html.Div(className='row', children=[
            html.Div(className='alert alert-warning', children=[
                html.Strong(children=[
                    'Importante!'
                ]),
                ' ',
                'A variável despesa máxima de campanha só foi disponibilizada a partir de 2002 e a variável '
                'idade do candidato a partir de 2014. Logo é normal que as mesmas sejam -1 antes desses anos.'
            ]),
        ]),
        html.Div(className='row', children=[
            x_axes_select, y_axes_select, bubble_size_select,
            grouping_select, regional_aggregation_select, political_aggregation_select,
        ]),
        html.Div(className='container-fluid', children=[
            chart
        ]),
        play_row
    ])
])
