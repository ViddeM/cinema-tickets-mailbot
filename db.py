from pony.orm import Database, PrimaryKey, Required

import config

db = Database()


class CinemaCity(db.Entity):
    alias = PrimaryKey(str)
    name = Required(str)


class Movie(db.Entity):
    movie_id = PrimaryKey(str)
    movie_name = Required(str)


db.bind(
    provider="postgres",
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
    database=config.POSTGRES_DB
)

db.generate_mapping(create_tables=True)
