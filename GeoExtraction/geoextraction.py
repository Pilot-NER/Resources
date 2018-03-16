import csv


class GeoExtraction:
    cities, states_abbrev, states_full, counties, city_aliases = list(), list(), list(), list(), list()

    with open("us_cities_states_counties.csv") as file:
        file = csv.reader(file)
        for row in file:
            if len(row) > 1:
                # print(row)
                row = [', '.join(row)]
            city, state_abbrev, state_full, county, city_alias = row[0].split("|")
            cities.append(city)
            states_abbrev.append(state_abbrev)
            states_full.append(state_full)
            counties.append(county)
            city_aliases.append(city_alias)

    def __init__(self, string):
        self.string = string

