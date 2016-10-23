import geojson

from flask import Flask, render_template
from db_utils import get_shelters, get_nearby

app = Flask(__name__)


@app.route('/')
def hello_world() -> object:
    return render_template('index.html')


@app.route('/shelters/')
def api_shelters() -> dict:
    shelters = get_shelters()
    return geojson.dumps(shelters)


@app.route('/nearby/<float:lat>/<float:lng>/<int:radius>/', methods=['GET'])
def api_nearby(lat, lng, radius) -> dict:
    nearby_tracks = get_nearby(lat, lng, radius)
    return geojson.dumps(nearby_tracks)

if __name__ == '__main__':
    app.run()
