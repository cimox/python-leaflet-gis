import geojson

from flask import Flask, render_template
from db_utils import get_shelters

app = Flask(__name__)


@app.route('/')
def hello_world() -> object:
    return render_template('index.html')


@app.route('/shelters/')
def api_shelters() -> dict:
    shelters = get_shelters()
    return geojson.dumps(shelters)


if __name__ == '__main__':
    app.run()
