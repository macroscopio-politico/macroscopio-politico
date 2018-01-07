import dash_html_components as html


def chart_menu():
    return html.Ul(className='nav justify-content-end', children=[
        html.Li(className='nav-item', children=[
            html.A(className='nav-link', href='/polls/line', children=['Linha']),
        ]),
        html.Ul(className='nav nav-pills mb-3', children=[
            html.Li(className='nav-item', children=[
                html.A(className='nav-link', href='/polls/bar', children=['Barra']),
            ]),
        ]),
        html.Ul(className='nav nav-pills mb-3', children=[
            html.Li(className='nav-item', children=[
                html.A(className='nav-link', href='/polls/bubble', children=['Bolha']),
            ]),
        ]),
        html.Ul(className='nav nav-pills mb-3', children=[
            html.Li(className='nav-item', children=[
                html.A(className='nav-link', href='/polls/pie', children=['Pizza']),
            ]),
        ]),
    ])
