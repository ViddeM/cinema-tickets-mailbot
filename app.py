from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from gather_data import load_cities

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/": {"origins":"*"}})

load_cities()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
