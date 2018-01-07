from cepesp import (
    CARGO
)


VALUE_AXES_OPTIONS = {
    'Qtd. Aptos': 'QTD_APTOS',
    'Qtd. Comparecimento': 'QTD_COMPARECIMENTO',
    'Qtd. Abstenções': 'QTD_ABSTENCOES',
    'Qtd. Votos Nominais': 'QT_VOTOS_NOMINAIS',
    'Qtd. Votos Brancos': 'QT_VOTOS_BRANCOS',
    'Qtd. Votos Nulos': 'QT_VOTOS_NULOS',
    'Qtd. Votos Legenda': 'QT_VOTOS_LEGENDA',
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
    'Prefeito': CARGO.PREFEITO,
    'Vereador': CARGO.VEREADOR,
}
