from flask import Response

import cepesp
from common.utils import csv_iterator
from server import server
from .data import fetch_dataframe


@server.route('/polls/data/presidente')
def generate_polls_presidente_csv():
    df = fetch_dataframe(cepesp.CARGO.PRESIDENTE)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/polls/data/governador')
def generate_polls_governador_csv():
    df = fetch_dataframe(cepesp.CARGO.GOVERNADOR)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/polls/data/depfederal')
def generate_polls_deputado_federal_csv():
    df = fetch_dataframe(cepesp.CARGO.DEPUTADO_FEDERAL)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/polls/data/depdistrital')
def generate_polls_deputado_distrital_csv():
    df = fetch_dataframe(cepesp.CARGO.DEPUTADO_DISTRITAL)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/polls/data/depestadual')
def generate_polls_deputado_estadual_csv():
    df = fetch_dataframe(cepesp.CARGO.DEPUTADO_ESTADUAL)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/polls/data/prefeito')
def generate_polls_prefeito_csv():
    df = fetch_dataframe(cepesp.CARGO.PREFEITO)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/polls/data/vereador')
def generate_polls_vereador_csv():
    df = fetch_dataframe(cepesp.CARGO.VEREADOR)
    return Response(csv_iterator(df), mimetype='text/csv')
