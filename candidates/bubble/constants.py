from cepesp import (
    CARGO
)


X_AXES_OPTIONS = {
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
Y_AXES_OPTIONS = X_AXES_OPTIONS
BUBBLE_SIZE_OPTIONS = X_AXES_OPTIONS
GROUPING_OPTIONS = {
    'UF': 'UF',
    'Gênero': 'DESCRICAO_SEXO',
    'Partido': 'SIGLA_PARTIDO',
    'Nacionalidade': 'DESCRICAO_NACIONALIDADE',
    'Estado Civil': 'DESCRICAO_ESTADO_CIVIL',
    'Grau de Instrução': 'DESCRICAO_GRAU_INSTRUCAO',
    'Situação da Candidatura': 'DESC_SIT_TOT_TURNO',
}
REGION_OPTIONS = {
    'UF': 'UF',
    'Mesorregião': 'NOME_MESO',
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
