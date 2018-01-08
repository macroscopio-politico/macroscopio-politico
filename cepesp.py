import hashlib
import os
import urllib
from tempfile import mkdtemp

import pandas as pd

baseURL = "http://cepesp.io/api/consulta/"
baseDir = os.path.dirname(__file__)
cache_dir = mkdtemp()


def add_filters(request,
                estado=None,
                numero_candidato=None,
                numero_partido=None,
                codigo_municipio=None):
    index = 0
    if estado is not None:
        request = add_uf_filter(request, estado)
    if numero_candidato is not None:
        request = add_filter(request, "NUMERO_CANDIDATO", numero_candidato,
                             index)
        index += 1
    if numero_partido is not None:
        request = add_filter(request, "NUMERO_PARTIDO", numero_partido, index)
        index += 1
    if codigo_municipio is not None:
        request = add_filter(request, "CODIGO_MUNICIPIO", codigo_municipio,
                             index)
        index += 1
    return request


def add_filter(request, column, value, index):
    return request + "&columns[{}][name]={}&columns[{}][search][value]={}".format(
        index, column, index, value)


def add_uf_filter(request, estado):
    return request + "&uf_filter={}".format(estado)


def filename(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest() + ".gz"


def save_cache(response, cache_filename):
    file_path = os.path.join(baseDir, "cache/" + cache_filename)
    with open(file_path, 'wb') as outfile:
        outfile.write(response.read())


def read_csv(cache_filename, request):
    cache_path = os.path.join(baseDir, "cache/" + cache_filename)
    cache_dir_path = os.path.dirname(cache_path)

    if not os.path.exists(cache_dir_path):
        os.mkdir(cache_dir_path)

    if not os.path.exists(cache_path):
        response = urllib.request.urlopen(baseURL + request)
        save_cache(response, cache_filename)
    return pd.read_csv(cache_path, sep=",", dtype=str)


def votos(cargo=1,
          ano=2014,
          agregacao_politica=1,
          agregacao_regional=0,
          estado=None,
          numero_candidato=None,
          numero_partido=None,
          codigo_municipio=None):
    request = "votos?cargo={}&ano={}&agregacao_politica={}&agregacao_regional={}&format=gzip".format(
        cargo, ano, agregacao_politica, agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido,
                          codigo_municipio)
    cache_filename = filename(request)
    return read_csv(cache_filename, request)


def consolidacao(cargo=1,
                 ano=2014,
                 agregacao_politica=4,
                 agregacao_regional=2,
                 estado=None,
                 numero_candidato=None,
                 numero_partido=None,
                 codigo_municipio=None):
    request = "tse?cargo={}&anos={}&agregacao_politica={}&agregacao_regional={" \
              "}&mun_filter=&uf_filter=&brancos=1&nulos=1&selected_columns%5B%5D=ANO_ELEICAO&selected_columns%5B%5D" \
              "=NUM_TURNO&selected_columns%5B%5D=UF&selected_columns%5B%5D=DESCRICAO_ELEICAO&selected_columns%5B%5D" \
              "=DESCRICAO_CARGO&selected_columns%5B%5D=QTD_APTOS&selected_columns%5B%5D=QTD_COMPARECIMENTO" \
              "&selected_columns%5B%5D=QTD_ABSTENCOES&selected_columns%5B%5D=QT_VOTOS_NOMINAIS&selected_columns%5B%5D" \
              "=QT_VOTOS_BRANCOS&selected_columns%5B%5D=QT_VOTOS_NULOS&selected_columns%5B%5D=QT_VOTOS_LEGENDA" \
              "&selected_columns%5B%5D=NOME_MICRO&selected_columns%5B%5D=NOME_MESO&selected_columns%5B%5D=NOME_MACRO" \
              "&selected_columns%5B%5D=NOME_MUNICIPIO&format=gzip".format(
        cargo, ano, agregacao_politica, agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido,
                          codigo_municipio)
    cache_filename = filename(request)
    return read_csv(cache_filename, request)


def candidatos(cargo=1,
               ano=2014,
               agregacao_politica=1,
               agregacao_regional=2,
               estado=None,
               numero_candidato=None,
               numero_partido=None,
               codigo_municipio=None):
    request = "candidatos?cargo={}&ano={}&agregacao_politica={}&agregacao_regional={}&format=gzip".format(
        cargo, ano, agregacao_politica, agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido,
                          codigo_municipio)
    cache_filename = filename(request)
    return read_csv(cache_filename, request)


def legendas(cargo=1,
             ano=2014,
             agregacao_politica=1,
             agregacao_regional=2,
             estado=None,
             numero_candidato=None,
             numero_partido=None,
             codigo_municipio=None):
    request = "legendas?cargo={}&ano={}&agregacao_politica={}&agregacao_regional={}&format=gzip".format(
        cargo, ano, agregacao_politica, agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido,
                          codigo_municipio)
    cache_filename = filename(request)
    return read_csv(cache_filename, request)


def votos_x_candidatos(cargo=1,
                       ano=2014,
                       agregacao_politica=1,
                       agregacao_regional=2,
                       estado=None,
                       numero_candidato=None):
    vot = votos(cargo, ano, agregacao_politica, agregacao_regional, estado,
                numero_candidato)
    cand = candidatos(cargo, ano, agregacao_politica, agregacao_regional,
                      estado, numero_candidato)
    return vot.set_index(
        ["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]).merge(
        cand.set_index(
            ["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]),
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["_x", "_y"]).reset_index()


def votos_x_legendas(cargo=1,
                     ano=2014,
                     agregacao_politica=1,
                     agregacao_regional=2,
                     estado=None,
                     numero_candidato=None):
    vot = votos(cargo, ano, agregacao_politica, agregacao_regional, estado,
                numero_candidato)
    leg = legendas(cargo, ano, agregacao_politica, agregacao_regional, estado,
                   numero_candidato)
    leg = leg.rename(columns={"NUMERO_PARTIDO": "NUMERO_CANDIDATO"})
    return vot.set_index(
        ["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]).merge(
        leg.set_index(
            ["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]),
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["_x", "_y"]).reset_index()


def candidato_x_legendas(cargo=1,
                         ano=2014,
                         agregacao_politica=1,
                         agregacao_regional=2,
                         estado=None,
                         numero_candidato=None):
    leg = legendas(cargo, ano, agregacao_politica, agregacao_regional, estado,
                   numero_candidato)
    cand = candidatos(cargo, ano, agregacao_politica, agregacao_regional,
                      estado, numero_candidato)
    return cand.set_index(["NUMERO_PARTIDO", "SIGLA_UE", "ANO_ELEICAO"]).merge(
        leg.set_index(["NUMERO_PARTIDO", "SIGLA_UE", "ANO_ELEICAO"]),
        how="left",
        left_index=True,
        right_index=True,
        suffixes=["_x", "_y"]).reset_index()


class CARGO:
    PRESIDENTE = 1
    SENADOR = 5
    GOVERNADOR = 3
    VEREADOR = 13
    PREFEITO = 11
    DEPUTADO_FEDERAL = 6
    DEPUTADO_ESTADUAL = 7
    DEPUTADO_DISTRITAL = 8


class AGR_REGIONAL:
    BRASIL = 0
    UF = 2
    MUNICIPIO = 6
    MUNZONA = 7
    ZONA = 8
    MACRO = 1
    MESO = 4
    MICRO = 5


class AGR_POLITICA:
    CANDIDATO = 1
    PARTIDO = 2
    COLIGACAO = 3
