import cepesp


def years_to_show(position):
    if position in ['Prefeito', 'Vereador', cepesp.CARGO.PREFEITO, cepesp.CARGO.VEREADOR]:
        return [2000, 2004, 2008, 2012, 2016]
    else:
        return [1998, 2002, 2006, 2010, 2014]


def csv_iterator(df):
    yield ','.join(df.columns) + '\n'

    for row in df.itertuples():
        yield ','.join([str(x) for x in row]) + '\n'
