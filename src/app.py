
import pandas as pd


def get_country(headline):
    return '-'


def get_city(headline):
    return '-'


def get_headlines_df(headlines):
    columns = ['headline', 'country', 'city']
    headlines_df = pd.DataFrame([
        [headline, 
         get_country(headline), 
         get_city(headline)] for headline in headlines
    ])
    return headlines_df


def read_headlines(source):
    with open(source) as handle:
        for line in handle:
            yield line.strip('\n')


df = get_headlines_df(read_headlines('../data/headlines.txt'))
