import locale
from locale import (
    atof,
    atoi,
)
from tempfile import mkdtemp

import pandas as pd
from joblib import Memory

import cepesp
from common.utils import years_to_show

cache_dir = mkdtemp()
memory = Memory(cachedir=cache_dir, verbose=0)
locale.setlocale(locale.LC_ALL, 'pt_BR')


@memory.cache
def fetch_dataframe(position):
    dfs_to_concat = []

    for year_to_show in years_to_show(position):
        df = cepesp.votos_x_candidatos(
            ano=year_to_show,
            cargo=position,
        )
        dfs_to_concat.append(df)

    votos_x_candidatos_df = pd.concat(dfs_to_concat)
    del dfs_to_concat

    del votos_x_candidatos_df['NOME_CANDIDATO']
    del votos_x_candidatos_df['EMAIL_CANDIDATO']
    del votos_x_candidatos_df['NUM_TITULO_ELEITORAL_CANDIDATO']

    votos_x_candidatos_df['NOME_PAIS'] = 'Brasil'
    votos_x_candidatos_df['DESPESA_MAX_CAMPANHA'] = votos_x_candidatos_df['DESPESA_MAX_CAMPANHA'].astype(str).apply(
        lambda x: atof(x))
    votos_x_candidatos_df['IDADE_DATA_ELEICAO'] = votos_x_candidatos_df['IDADE_DATA_ELEICAO'].astype(str).apply(
        lambda x: atof(x))
    votos_x_candidatos_df['QTDE_VOTOS'] = votos_x_candidatos_df['QTDE_VOTOS'].astype(str).apply(lambda x: atoi(x))
    votos_x_candidatos_df['QTD_CANDIDATOS'] = 1
    votos_x_candidatos_df['QTD_CANDIDATOS_ELEITOS'] = votos_x_candidatos_df['DESC_SIT_TOT_TURNO'].apply(
        lambda x: 1 if x == 'ELEITO' else 0
    )
    votos_x_candidatos_df['QTD_CANDIDATOS_N_ELEITOS'] = votos_x_candidatos_df['DESC_SIT_TOT_TURNO'].apply(
        lambda x: 1 if x != 'ELEITO' else 0
    )

    return votos_x_candidatos_df


def add_data(votos_x_candidatos_df, columns):
    votos_x_candidatos_mean_df = votos_x_candidatos_df[columns + [
        'DESPESA_MAX_CAMPANHA', 'IDADE_DATA_ELEICAO', 'QTDE_VOTOS'
    ]].groupby(columns).mean()

    votos_x_candidatos_std_df = votos_x_candidatos_df[columns + [
        'DESPESA_MAX_CAMPANHA', 'IDADE_DATA_ELEICAO', 'QTDE_VOTOS'
    ]].groupby(columns).std()

    del votos_x_candidatos_df['DESPESA_MAX_CAMPANHA']
    del votos_x_candidatos_df['IDADE_DATA_ELEICAO']

    votos_x_candidatos_sum_df = votos_x_candidatos_df[columns + [
        'QTD_CANDIDATOS', 'QTD_CANDIDATOS_ELEITOS', 'QTD_CANDIDATOS_N_ELEITOS', 'QTDE_VOTOS',
    ]].groupby(columns).sum()

    votos_x_candidatos_df = votos_x_candidatos_df.groupby(columns).count()

    votos_x_candidatos_df['QTD_CANDIDATOS'] = votos_x_candidatos_sum_df['QTD_CANDIDATOS']
    votos_x_candidatos_df['QTD_CANDIDATOS_ELEITOS'] = votos_x_candidatos_sum_df['QTD_CANDIDATOS_ELEITOS']
    votos_x_candidatos_df['QTD_CANDIDATOS_N_ELEITOS'] = votos_x_candidatos_sum_df['QTD_CANDIDATOS_N_ELEITOS']
    votos_x_candidatos_df['QTDE_VOTOS'] = votos_x_candidatos_sum_df['QTDE_VOTOS']
    votos_x_candidatos_df['MEAN_QTDE_VOTOS'] = votos_x_candidatos_mean_df['QTDE_VOTOS']
    votos_x_candidatos_df['MEAN_DESPESA_MAX_CAMPANHA'] = votos_x_candidatos_mean_df['DESPESA_MAX_CAMPANHA']
    votos_x_candidatos_df['MEAN_IDADE_DATA_ELEICAO'] = votos_x_candidatos_mean_df['IDADE_DATA_ELEICAO']
    votos_x_candidatos_df['STD_QTDE_VOTOS'] = votos_x_candidatos_std_df['QTDE_VOTOS']
    votos_x_candidatos_df['STD_DESPESA_MAX_CAMPANHA'] = votos_x_candidatos_std_df['DESPESA_MAX_CAMPANHA']
    votos_x_candidatos_df['STD_IDADE_DATA_ELEICAO'] = votos_x_candidatos_std_df['IDADE_DATA_ELEICAO']

    return votos_x_candidatos_df


def add_hover_data(votos_x_candidatos_df, percentage_column):
    percentage_sum = votos_x_candidatos_df[percentage_column].sum()
    votos_x_candidatos_df['TEXT_PERCENTAGE'] = votos_x_candidatos_df.loc[:, percentage_column] / percentage_sum

    return votos_x_candidatos_df


@memory.cache
def process_data(position, bubble_size_column, regional_aggregation_column, grouping_column):
    votos_x_candidatos_df = fetch_dataframe(position)

    columns = ['ANO_ELEICAO', 'NUM_TURNO']

    if grouping_column != regional_aggregation_column:
        columns.append(regional_aggregation_column)

    columns.append(grouping_column)

    votos_x_candidatos_df = add_data(votos_x_candidatos_df, columns)
    votos_x_candidatos_df = add_hover_data(votos_x_candidatos_df, bubble_size_column)

    years = votos_x_candidatos_df.index.levels[0]
    return votos_x_candidatos_df.reset_index(level=['NUM_TURNO', grouping_column]), years



@memory.cache
def process_line_data(position, x_column, y_column, grouping_column):
    votos_x_candidatos_df = fetch_dataframe(position)

    columns = [x_column, grouping_column]

    votos_x_candidatos_df = add_data(votos_x_candidatos_df, columns)
    votos_x_candidatos_df = add_hover_data(votos_x_candidatos_df, y_column)

    years = votos_x_candidatos_df.index.levels[0]
    return votos_x_candidatos_df.reset_index(level=[x_column]), years


@memory.cache
def process_bar_data(position, x_column, y_column, grouping_column):
    votos_x_candidatos_df = fetch_dataframe(position)

    columns = [x_column, grouping_column]

    votos_x_candidatos_df = add_data(votos_x_candidatos_df, columns)
    votos_x_candidatos_df = add_hover_data(votos_x_candidatos_df, y_column)

    years = votos_x_candidatos_df.index.levels[0]
    return votos_x_candidatos_df.reset_index(level=[x_column]), years


@memory.cache
def process_pie_data(position, value_column, grouping_column):
    votos_x_candidatos_df = fetch_dataframe(position)

    columns = [grouping_column]

    votos_x_candidatos_df = add_data(votos_x_candidatos_df, columns)
    votos_x_candidatos_df = add_hover_data(votos_x_candidatos_df, value_column)

    years = votos_x_candidatos_df.index
    return votos_x_candidatos_df, years
