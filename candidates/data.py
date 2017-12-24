import locale
from locale import (
    atof,
    atoi,
)
from tempfile import mkdtemp

import pandas as pd
from joblib import Memory

import cepesp

cache_dir = mkdtemp()
memory = Memory(cachedir=cache_dir, verbose=0)
locale.setlocale(locale.LC_ALL, 'pt_BR')


def years_to_show(position):
    if position in ['Prefeito', 'Vereador', cepesp.CARGO.PREFEITO, cepesp.CARGO.VEREADOR]:
        return [2000, 2004, 2008, 2012, 2016]
    else:
        return [1998, 2002, 2006, 2010, 2014]


@memory.cache
def process_data(position, grouping_column):
    dfs_to_concat = []

    for year_to_show in years_to_show(position):
        df = cepesp.votos_x_candidatos(
            ano=year_to_show,
            cargo=position,
        )
        dfs_to_concat.append(df)

    votos_x_candidatos_df = pd.concat(dfs_to_concat)
    del dfs_to_concat

    columns = ['ANO_ELEICAO', 'NUM_TURNO', grouping_column]

    votos_x_candidatos_df['DESPESA_MAX_CAMPANHA'] = votos_x_candidatos_df['DESPESA_MAX_CAMPANHA'].astype(str).apply(lambda x: atof(x))
    votos_x_candidatos_df['IDADE_DATA_ELEICAO'] = votos_x_candidatos_df['IDADE_DATA_ELEICAO'].astype(str).apply(lambda x: atof(x))
    votos_x_candidatos_df['QTDE_VOTOS'] = votos_x_candidatos_df['QTDE_VOTOS'].astype(str).apply(lambda x: atoi(x))
    votos_x_candidatos_df['QTD_CANDIDATOS'] = 1
    votos_x_candidatos_df['QTD_CANDIDATOS_ELEITOS'] = votos_x_candidatos_df['DESC_SIT_TOT_TURNO'].apply(
        lambda x: 1 if x == 'ELEITO' else 0
    )
    votos_x_candidatos_df['QTD_CANDIDATOS_N_ELEITOS'] = votos_x_candidatos_df['DESC_SIT_TOT_TURNO'].apply(
        lambda x: 1 if x != 'ELEITO' else 0
    )

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

    years = votos_x_candidatos_df.index.levels[0]
    return votos_x_candidatos_df.reset_index(level=['NUM_TURNO']), years
