# -*- coding: utf-8 -*-
import functools

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from .constants import (
    BUBBLE_CATEGORY_OPTIONS,
    BUBBLE_SIZE_OPTIONS,
    POSITION_OPTIONS,
    X_AXES_OPTIONS,
    Y_AXES_OPTIONS,
)
from .data import (
    process_data,
    years_to_show,
)

config = dict(
    current_x_axes='Qtd. Votos',
    current_y_axes='Média da Despesa Máx. de Campanha',
    current_bubble_size='Qtd. Candidatos',
    current_bubble_color='Gênero',
    current_political_aggregation='Presidente',
    years=None,
    source=None
)


chart = dcc.Graph(
    id='candidates-chart', style={'margin': '20px 0px'},
)


def plot_figure(data):
    x_column = X_AXES_OPTIONS[config['current_x_axes']]
    y_column = Y_AXES_OPTIONS[config['current_y_axes']]
    bubble_size_column = BUBBLE_SIZE_OPTIONS[config['current_bubble_size']]

    size_percentage_sum = data[bubble_size_column].sum()
    data['text_percentage'] = (data[bubble_size_column] / size_percentage_sum)
    regional_aggregation_column = BUBBLE_CATEGORY_OPTIONS[config['current_bubble_color']]    

    figure = dict(
        data=[],
        layout=go.Layout(
            title='{} x {}<br>para o cargo de {} no ano de {}'.format(
                config['current_x_axes'], config['current_y_axes'], config['current_political_aggregation'], config['current_year']
            ),
            xaxis={'type': 'log', 'title': config['current_x_axes']},
            yaxis={'title': config['current_y_axes']},
            margin={'l': 60, 'b': 40, 't': 80, 'r': 0},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )

    default_size_ref = 2 * data[bubble_size_column].max() / (100**2)

    for region_name in data[regional_aggregation_column].unique():
        regional_aggregation_df = data[data[regional_aggregation_column] == region_name]

        plot_data = go.Scattergl(
            x=regional_aggregation_df[x_column].tolist(),
            y=regional_aggregation_df[y_column].tolist(),
            text=regional_aggregation_df.apply(
                lambda row: '{}<br>Turno: {}º<br>{}: {} ({:.2%})'.format(
                    str(row[regional_aggregation_column]),
                    str(row['NUM_TURNO']),
                    config['current_bubble_size'],
                    str(row[bubble_size_column]),
                    row['text_percentage'],
                ),
                axis=1
            ).values,
            mode='markers',
            opacity=0.7,
            marker={
                'sizemode': 'area',
                'sizeref': default_size_ref,
                'sizemin': 5,
                'opacity': 0.7,
                'size': regional_aggregation_df[bubble_size_column],
            },
            name=region_name
        )

        figure['data'].append(plot_data)
    
    return figure


@functools.lru_cache()
def update(current_year=None, x_axes=None, y_axes=None, bubble_size=None,
           bubble_color=None, political_aggregation=None):
    if x_axes is None:
        x_axes = config['current_x_axes']

    if y_axes is None:
        y_axes = config['current_y_axes']

    if bubble_size is None:
        bubble_size = config['current_bubble_size']

    if bubble_color is None:
        bubble_color = config['current_bubble_color']

    if political_aggregation is None:
        political_aggregation = config['current_political_aggregation']

    votos_df, years = process_data(
        bubble_color_column=BUBBLE_CATEGORY_OPTIONS[bubble_color],
        position=POSITION_OPTIONS[political_aggregation])

    if current_year is None:
        current_year = years[0]

    if int(current_year) < int(years[0]):
        current_year = years[0]

    data = {}

    for year in years:
        data[year] = votos_df[votos_df['ANO_ELEICAO'] == year]

    config['current_year'] = current_year
    config['current_x_axes'] = x_axes
    config['current_y_axes'] = y_axes
    config['current_bubble_size'] = bubble_size
    config['current_bubble_color'] = bubble_color
    config['current_political_aggregation'] = political_aggregation
    config['years'] = years
    config['data'] = data

    return plot_figure(data[current_year])


x_axes_select = html.Div(className='col', children=[
    html.Label('Eixo X:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in X_AXES_OPTIONS.keys()
        ],
        value=config['current_x_axes'],
        clearable=False,
        id='x-axes-select'
    ),
])


y_axes_select = html.Div(className='col', children=[
    html.Label('Eixo Y:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in Y_AXES_OPTIONS.keys()
        ],
        value=config['current_y_axes'],
        clearable=False,
        id='y-axes-select'
    ),
])


bubble_size_select = html.Div(className='col', children=[
    html.Label('Tamanho da Bolha:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in BUBBLE_SIZE_OPTIONS.keys()
        ],
        value=config['current_bubble_size'],
        clearable=False,
        id='bubble-size-select'
    ),
])


bubble_color_select = html.Div(className='col', children=[
    html.Label('Cor da Bolha:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in BUBBLE_CATEGORY_OPTIONS.keys()
        ],
        value=config['current_bubble_color'],
        clearable=False,
        id='bubble-color-select'
    ),
])


political_aggregation_select = html.Div(className='col', children=[
    html.Label('Agregação Politica:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in POSITION_OPTIONS.keys()
        ],
        value=config['current_political_aggregation'],
        clearable=False,
        id='political-aggregation-select'
    ),
])


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
            x_axes_select, y_axes_select, bubble_size_select
        ]),
        html.Div(className='row', children=[
            bubble_color_select, political_aggregation_select,
        ]),
        html.Div(className='container-fluid', children=[
            chart
        ]),
        play_row
    ])
])
