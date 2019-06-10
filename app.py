import datetime
import threading
import time

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from gather_data import update_database
from quickstart import get_shows

from pytz import timezone

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/": {"origins": "*"}})


def run_update():
    while (True):
        update_database()
        # Update once every hour
        time.sleep(3600)


threading.Thread(target=run_update)

timezone = timezone("Europe/Stockholm")
shows = get_shows("NCG997491", "HD", "Röda Kvarn i Halmstad", datetime.datetime(year=2019, month=4, day=24))

for show in shows:
    print(show.movie.name + " is shown in halmstad on " + str(show.date.astimezone(timezone)))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
