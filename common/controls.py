import dash_core_components as dcc
import dash_html_components as html


def value_axes_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
        html.Label('Eixo:'),
        dcc.Dropdown(
            options=[
                {'label': label, 'value': label}
                for label in options.keys()
            ],
            value=value,
            clearable=False,
            id='value-axes-select'
        ),
    ])


def x_axes_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
        html.Label('Eixo X:'),
        dcc.Dropdown(
            options=[
                {'label': label, 'value': label}
                for label in options.keys()
            ],
            value=value,
            clearable=False,
            id='x-axes-select'
        ),
    ])


def y_axes_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
    html.Label('Eixo Y:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in options.keys()
        ],
        value=value,
        clearable=False,
        id='y-axes-select'
    ),
])


def grouping_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
    html.Label('Agrupar por:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in options.keys()
        ],
        value=value,
        clearable=False,
        id='grouping-select'
    ),
])


def regional_aggregation_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
        html.Label('Agregação Regional:'),
        dcc.Dropdown(
            options=[
                {'label': label, 'value': label}
                for label in options.keys()
            ],
            value=value,
            clearable=False,
            id='regional-aggregation-select'
        ),
    ])


def political_aggregation_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
        html.Label('Agregação Politica:'),
        dcc.Dropdown(
            options=[
                {'label': label, 'value': label}
                for label in options.keys()
            ],
            value=value,
            clearable=False,
            id='political-aggregation-select'
        ),
    ])


def bubble_size_select(value, options):
    return html.Div(className='col-md-4 col-sm-6 col-xs-12', children=[
    html.Label('Tamanho da Bolha:'),
    dcc.Dropdown(
        options=[
            {'label': label, 'value': label}
            for label in options.keys()
        ],
        value=value,
        clearable=False,
        id='bubble-size-select'
    ),
])
