import locale
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
def process_data(position, regional_aggregation_column, grouping_column):
    dfs_to_concat = []

    for year_to_show in years_to_show(position):
        df = cepesp.consolidacao(
            ano=year_to_show,
            cargo=position,
            agregacao_regional=cepesp.AGR_REGIONAL.MUNICIPIO
        )

        dfs_to_concat.append(df)

    votos_df = pd.concat(dfs_to_concat)

    votos_df['QTD_APTOS'] = votos_df.QTD_APTOS.astype(int)
    votos_df['QTD_COMPARECIMENTO'] = votos_df.QTD_COMPARECIMENTO.astype(int)
    votos_df['QTD_ABSTENCOES'] = votos_df.QTD_ABSTENCOES.astype(int)
    votos_df['QT_VOTOS_NOMINAIS'] = votos_df.QT_VOTOS_NOMINAIS.astype(int)
    votos_df['QT_VOTOS_BRANCOS'] = votos_df.QT_VOTOS_BRANCOS.astype(int)
    votos_df['QT_VOTOS_NULOS'] = votos_df.QT_VOTOS_NULOS.astype(int)
    votos_df['QT_VOTOS_LEGENDA'] = votos_df.QT_VOTOS_LEGENDA.astype(int)

    columns = ['ANO_ELEICAO', 'NUM_TURNO']

    if grouping_column != regional_aggregation_column:
        columns.append(regional_aggregation_column)

    columns.append(grouping_column)

    votos_df = votos_df.groupby(columns).sum()

    years = votos_df.index.levels[0]
    return votos_df.reset_index(level=['NUM_TURNO', grouping_column]), years
