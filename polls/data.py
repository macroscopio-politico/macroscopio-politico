import locale
from locale import (
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
        df = cepesp.consolidacao(
            ano=year_to_show,
            cargo=position,
            agregacao_regional=cepesp.AGR_REGIONAL.MUNICIPIO
        )

        dfs_to_concat.append(df)

    votos_df = pd.concat(dfs_to_concat)

    votos_df['NOME_PAIS'] = 'Brasil'
    votos_df['QTD_APTOS'] = votos_df.QTD_APTOS.astype(str).apply(lambda x: atoi(x))
    votos_df['QTD_COMPARECIMENTO'] = votos_df.QTD_COMPARECIMENTO.astype(str).apply(lambda x: atoi(x))
    votos_df['QTD_ABSTENCOES'] = votos_df.QTD_ABSTENCOES.astype(str).apply(lambda x: atoi(x))
    votos_df['QT_VOTOS_NOMINAIS'] = votos_df.QT_VOTOS_NOMINAIS.astype(str).apply(lambda x: atoi(x))
    votos_df['QT_VOTOS_BRANCOS'] = votos_df.QT_VOTOS_BRANCOS.astype(str).apply(lambda x: atoi(x))
    votos_df['QT_VOTOS_NULOS'] = votos_df.QT_VOTOS_NULOS.astype(str).apply(lambda x: atoi(x))
    votos_df['QT_VOTOS_LEGENDA'] = votos_df.QT_VOTOS_LEGENDA.astype(str).apply(lambda x: atoi(x))

    return votos_df


def add_data(votos_df, columns):
    return votos_df.groupby(columns).sum()


def add_hover_data(votos_df, percentage_column):
    percentage_sum = votos_df[percentage_column].sum()
    votos_df['TEXT_PERCENTAGE'] = votos_df.loc[:, percentage_column] / percentage_sum

    return votos_df


@memory.cache
def process_data(position, bubble_size_column, regional_aggregation_column, grouping_column):
    votos_df = fetch_dataframe(position)

    columns = ['ANO_ELEICAO', 'NUM_TURNO']

    if grouping_column != regional_aggregation_column:
        columns.append(regional_aggregation_column)

    columns.append(grouping_column)

    votos_df = add_data(votos_df, columns)
    votos_df = add_hover_data(votos_df, bubble_size_column)

    years = votos_df.index.levels[0]
    return votos_df.reset_index(level=['NUM_TURNO', grouping_column]), years


@memory.cache
def process_line_data(position, x_column, y_column, grouping_column):
    votos_df = fetch_dataframe(position)

    columns = [x_column, grouping_column]

    votos_df = add_data(votos_df, columns)
    votos_df = add_hover_data(votos_df, y_column)

    years = votos_df.index.levels[0]
    return votos_df.reset_index(level=[x_column]), years


@memory.cache
def process_bar_data(position, x_column, y_column, grouping_column):
    votos_df = fetch_dataframe(position)

    columns = [x_column, grouping_column]

    votos_df = add_data(votos_df, columns)
    votos_df = add_hover_data(votos_df, y_column)

    years = votos_df.index
    return votos_df.reset_index(level=[x_column]), years


@memory.cache
def process_pie_data(position, value_column, grouping_column):
    votos_df = fetch_dataframe(position)

    columns = [grouping_column]

    votos_df = add_data(votos_df, columns)
    votos_df = add_hover_data(votos_df, value_column)

    years = votos_df.index
    return votos_df, years
