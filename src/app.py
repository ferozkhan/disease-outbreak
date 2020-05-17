
import json
import geonamescache
import pandas as pd
import numpy as np
import re
import unidecode as unidecode


def get_headlines(source):
    with open(source) as handle:
        for line in handle:
            yield unidecode.unidecode(line.strip('\n'))


def find_match(text, regex):
    found = re.search(regex, text)
    if found:
        return found.group(0)
    return None


def get_city_name(headline, regex):
    return find_match(headline, regex)


def get_country_name(headline, regex):
    return find_match(headline, regex)


gc = geonamescache.GeonamesCache()
countries = [country["name"] for country in gc.get_countries().values()]
cities = [city["name"] for city in gc.get_cities().values()]

coutries_accent_map = {
    unidecode.unidecode(country): country for country in countries
}

cities_accent_map = {
    unidecode.unidecode(city): city for city in cities
}

unaccented_countries = set(coutries_accent_map.keys())
unaccented_cities = list(cities_accent_map.keys())

unaccented_countries = sorted(unaccented_countries, key=lambda x: len(x), reverse=True)
unaccented_cities = sorted(unaccented_cities, key=lambda x: len(x), reverse=True)

city_regex = r'\b|\b'.join(unaccented_cities)
country_regex = r'\b|\b'.join(unaccented_countries)

headlines = get_headlines('../data/headlines.txt')
headlines_cities_countries = [
    dict(headline=headline,
         countries=get_country_name(headline, country_regex),
         cities=get_city_name(headline, city_regex)) for headline in headlines]

with open('../data/headlines_cities_countries.json', 'w') as fout:
    fout.write(json.dumps(headlines_cities_countries))

with open('../data/unaccented_countries.json', 'w') as fout:
    fout.write(json.dumps(unaccented_countries))

with open('../data/unaccented_cities.json', 'w') as fout:
    fout.write(json.dumps(unaccented_cities))

data = pd.read_json('../data/headlines_cities_countries.json')
data = data.replace({None: np.nan})
data.head()