from cepesp import (
    CARGO
)


X_AXES_OPTIONS = {
    'Qtd. Aptos': 'QTD_APTOS',
    'Qtd. Comparecimento': 'QTD_COMPARECIMENTO',
    'Qtd. Abstenções': 'QTD_ABSTENCOES',
    'Qtd. Votos Nominais': 'QT_VOTOS_NOMINAIS',
    'Qtd. Votos Brancos': 'QT_VOTOS_BRANCOS',
    'Qtd. Votos Nulos': 'QT_VOTOS_NULOS',
    'Qtd. Votos Legenda': 'QT_VOTOS_LEGENDA',
}
Y_AXES_OPTIONS = X_AXES_OPTIONS
BUBBLE_SIZE_OPTIONS = X_AXES_OPTIONS
BUBBLE_CATEGORY_OPTIONS = {
    'UF': 'UF',
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
