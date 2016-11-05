import geojson

from db_utils import Postis
from flask import Flask, render_template

app = Flask(__name__)
db = Postis('postgres', 'postgres', 5432, 'localhost')

@app.route('/')
def hello_world() -> object:
    return render_template('index.html')


@app.route('/shelters/')
def api_shelters() -> dict:
    shelters = db.get_shelters()
    return geojson.dumps(shelters)


@app.route('/nearby/<float:lat>/<float:lng>/<int:radius>/', methods=['GET'])
def api_nearby(lat, lng, radius) -> dict:
    nearby_tracks = db.get_nearby(lat, lng, radius)
    return geojson.dumps(nearby_tracks)


@app.route('/nearby-city/<int:radius>/<float:lat>/<float:lng>/', methods=['GET'])
def api_nearby_city(lat, lng, radius) -> dict:
    nearby_city = db.get_nearby_city({'lat': lat, 'lng': lng}, radius)
    return geojson.dumps(nearby_city)


@app.route('/spring-onway/<int:radius>/<float:lat>/<float:lng>/<int:radius_water>/<string:req_type>/', methods=['GET'])
def api_spring_onway(lat, lng, radius, radius_water, req_type):
    features = db.get_track_with_spring_onway({'lat': lat, 'lng': lng}, radius, radius_water)
    if req_type == 'tracks':  #TODO: change this so only 1 request is necessary
        return geojson.dumps(features[0])
    elif req_type == 'springs':
        return geojson.dumps(features[1])
    else:
        return geojson.dumps('')


if __name__ == '__main__':
    app.run()
