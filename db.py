import datetime

from pony.orm import Database, PrimaryKey, Required, Set

import config

db = Database()


class CinemaCity(db.Entity):
    alias = PrimaryKey(str)
    name = Required(str)
    cinemas = Set("Cinema")


class Movie(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)
    shows = Set("Show")


class Cinema(db.Entity):
    name = Required(str)
    city = Required(CinemaCity)
    rooms = Set("CinemaRoom")
    PrimaryKey(name, city)


class CinemaRoom(db.Entity):
    name = Required(str)
    cinema = Required(Cinema)
    shows = Set("Show")
    PrimaryKey(name, cinema)


class Show(db.Entity):
    movie = Required(Movie)
    room = Required(CinemaRoom)
    date = Required(datetime.datetime)
    PrimaryKey(movie, room, date)


db.bind(
    provider="postgres",
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    database=config.POSTGRES_DB
)

db.generate_mapping(create_tables=True)
