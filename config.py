import os

POSTGRES_USER = os.environ.get("CINEMA_POSTGRES_USER", "cinema")
POSTGRES_PASSWORD = os.environ.get("CINEMA_POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.environ.get("CINEMA_POSTGRES_HOST", 'localhost')
POSTGRES_PORT = os.environ.get("CINEMA_POSTGRES_PORT", '5432')
POSTGRES_DB = os.environ.get("CINEMA_POSTGRES_DB", 'cinema')