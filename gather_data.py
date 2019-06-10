import datetime
import json
import pytz

import requests
from pony.orm import db_session

from db import CinemaCity, Movie, CinemaRoom, Cinema, Show


@db_session
def update_database():
    with open("cities.json") as json_file:
        cities = json.load(json_file)
        print(str(len(cities["cities"])) + " cities loaded")

        city_aliases = []
        for city in cities["cities"]:
            city_aliases.append(city["alias"])
            if not CinemaCity.get(alias=city["alias"]):
                CinemaCity(alias=city["alias"], name=city["name"])

        city_aliases = ["HD"]
        shows = load_shows(city_aliases)
        movies = load_movies(shows)
        for movie in movies:
            movie_id = movie["ncgId"]
            if not Movie.get(id=movie_id):
                Movie(id=movie_id, name=movie["title"])

        for city in shows:
            for show in shows[city]:
                cinema = show["ct"]
                room = show["st"]
                movie = show["mId"]
                date = show["utc"]
                formatted_date = pytz.utc.localize(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"))

                cinema_obj = Cinema.get(name=cinema, city=city)
                if not cinema_obj:
                    cinema_obj = Cinema(name=cinema, city=city)
                room_obj = CinemaRoom.get(name=room, cinema=cinema_obj)
                if not room_obj:
                    room_obj = CinemaRoom(name=room, cinema=cinema_obj)
                if not Show.get(movie=movie, room=room_obj, date=formatted_date):
                    Show(movie=movie, room=room_obj, date=formatted_date)


def load_shows(city_aliases):
    # now contains all the shows in the country!
    shows = {}
    num_shows = 0
    for city in city_aliases:
        json = requests.get(
            url="https://www.filmstaden.se/api/v2/show/stripped/sv/1/1024?filter.countryAlias=se&filter.cityAlias=" + city).json()
        city_shows = json["items"]
        shows[city] = city_shows
        num_shows += json["totalNbrOfItems"]

    print("Loaded " + str(num_shows) + " shows!")
    return shows


def load_movies(shows):
    show_ids = []
    for city in shows:
        for show in shows[city]:
            show_movie_id = show["mId"]
            if show_movie_id not in show_ids:
                show_ids.append(show_movie_id)

    index = 0
    max_movies_per_request = 25
    movies = []
    show_ids_short = []
    for id in show_ids:
        show_ids_short.append(id)
        index += 1
        if index >= max_movies_per_request:
            movies = get_movies(show_ids_short, movies)
            show_ids_short = []
            index = 0
    movies = get_movies(show_ids_short, movies)

    print("Loaded " + str(len(movies)) + " movies!")
    return movies


def get_movies(show_ids_short, movies):
    movies_params = {"filter.movieNcgIds": show_ids_short}
    movies_json = requests.get(url="https://www.filmstaden.se/api/v2/movie/sv/1/25/",
                               params=movies_params).json()
    return movies + movies_json["items"]
