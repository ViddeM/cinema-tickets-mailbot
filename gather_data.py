import json

from pony.orm import db_session

from db import CinemaCity


@db_session
def load_cities():
    with open("cities.json") as json_file:
        cities = json.load(json_file)
        for city in cities:
            CinemaCity(alias=city["alias"], name=city["alias"])

