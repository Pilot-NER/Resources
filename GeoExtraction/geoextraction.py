import csv
import copy

cities, states_abbrev, states_full, counties, city_aliases = list(), list(), list(), list(), list()

with open("./GeoExtraction/us_cities_states_counties.csv") as file:
    file = csv.reader(file)
    next(file)  # skip the header
    for row in file:
        if len(row) > 1:
            # print(row)
            row = [', '.join(row)]
        city, state_abbrev, state_full, county, city_alias = row[0].split("|")
        cities.append(city.lower())
        states_abbrev.append(state_abbrev.lower())
        states_full.append(state_full.lower())
        counties.append(county.lower())
        city_aliases.append(city_alias.lower())

class GeoExtraction:

    def __init__(self, string):
        self.string = string.lower()
        self.city = {each for each in cities if each in self.string}
        self.state_abbrev = {each for each in states_abbrev if each in self.string}
        self.state_full = {each for each in states_full if each in self.string}
        self.county = {each for each in counties if each in self.string}
        self.city_alias = {each for each in city_aliases if each in self.string}

    def location(self):
        d = {"city": self.city, "state_abbrev": self.state_abbrev, "state_full": self.state_full, "county":self.county, "city_alias":self.city_alias}
        d_copy = copy.deepcopy(d)
        for k, v in d_copy.items():
            if not v:
                del d[k]

        return d



