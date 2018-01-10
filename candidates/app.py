from flask import Response

import cepesp
from common.utils import csv_iterator
from server import server
from .data import fetch_dataframe


@server.route('/candidates/data/presidente')
def generate_candidates_presidente_csv():
    df = fetch_dataframe(cepesp.CARGO.PRESIDENTE)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/candidates/data/governador')
def generate_candidates_governador_csv():
    df = fetch_dataframe(cepesp.CARGO.GOVERNADOR)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/candidates/data/depfederal')
def generate_candidates_deputado_federal_csv():
    df = fetch_dataframe(cepesp.CARGO.DEPUTADO_FEDERAL)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/candidates/data/depdistrital')
def generate_candidates_deputado_distrital_csv():
    df = fetch_dataframe(cepesp.CARGO.DEPUTADO_DISTRITAL)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/candidates/data/depestadual')
def generate_deputado_estadual_csv():
    df = fetch_dataframe(cepesp.CARGO.DEPUTADO_ESTADUAL)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/candidates/data/prefeito')
def generate_candidates_prefeito_csv():
    df = fetch_dataframe(cepesp.CARGO.PREFEITO)
    return Response(csv_iterator(df), mimetype='text/csv')


@server.route('/candidates/data/vereador')
def generate_candidates_vereador_csv():
    df = fetch_dataframe(cepesp.CARGO.VEREADOR)
    return Response(csv_iterator(df), mimetype='text/csv')
