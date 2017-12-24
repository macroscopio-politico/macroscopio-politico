from cepesp import (
    CARGO
)


X_AXES_OPTIONS = {
    'Ano': 'ANO_ELEICAO',
}
Y_AXES_OPTIONS = {
    'Qtd. Comparecimento': 'QTD_COMPARECIMENTO',
    'Qtd. Abstenções': 'QTD_ABSTENCOES',
    'Qtd. Votos Nominais': 'QT_VOTOS_NOMINAIS',
    'Qtd. Votos Brancos': 'QT_VOTOS_BRANCOS',
    'Qtd. Votos Nulos': 'QT_VOTOS_NULOS',
    'Qtd. Votos Legenda': 'QT_VOTOS_LEGENDA',
}
GROUPING_OPTIONS = {
    'UF': 'UF',
    'Mesorregião': 'NOME_MESO',
    'Macrorregião': 'NOME_MACRO',
}
POSITION_OPTIONS = {
    'Presidente': CARGO.PRESIDENTE,
    'Governador': CARGO.GOVERNADOR,
    'Senador': CARGO.SENADOR,
    'Deputado Federal': CARGO.DEPUTADO_FEDERAL,
    'Deputado Estadual': CARGO.DEPUTADO_ESTADUAL,
    'Deputado Distrital': CARGO.DEPUTADO_DISTRITAL,
    'Prefeito': CARGO.PREFEITO,
    'Vereador': CARGO.VEREADOR,
}
