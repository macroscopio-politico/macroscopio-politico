from cepesp import (
    CARGO
)


VALUE_AXES_OPTIONS = {
    'Qtd. Votos': 'QTDE_VOTOS',
    'Média da Qtd. Votos': 'MEAN_QTDE_VOTOS',
    'Desvio Padrão da Qtd. Votos': 'STD_QTDE_VOTOS',
    'Média da Despesa Máx. de Campanha': 'MEAN_DESPESA_MAX_CAMPANHA',
    'Desvio Padrão da Despesa Máx. de Campanha': 'STD_DESPESA_MAX_CAMPANHA',
    'Média da Idade do Candidato': 'MEAN_IDADE_DATA_ELEICAO',
    'Desvio Padrão da Idade do Candidato': 'STD_IDADE_DATA_ELEICAO',
    'Qtd. Candidatos': 'QTD_CANDIDATOS',
    'Qtd. Candidatos Eleitos': 'QTD_CANDIDATOS_ELEITOS',
    'Qtd. Candidatos Não Eleitos': 'QTD_CANDIDATOS_N_ELEITOS',
}
GROUPING_OPTIONS = {
    'UF': 'UF',
    'Macrorregião': 'NOME_MACRO',
    'Brasil': 'NOME_PAIS',
}
POSITION_OPTIONS = {
    'Presidente': CARGO.PRESIDENTE,
    'Governador': CARGO.GOVERNADOR,
    'Senador': CARGO.SENADOR,
    'Deputado Federal': CARGO.DEPUTADO_FEDERAL,
    'Deputado Estadual': CARGO.DEPUTADO_ESTADUAL,
    'Deputado Distrital': CARGO.DEPUTADO_DISTRITAL,
    # 'Prefeito': CARGO.PREFEITO,  # There are some problems in the received CSVs
    # 'Vereador': CARGO.VEREADOR,  # There are some problems in the received CSVs
}
