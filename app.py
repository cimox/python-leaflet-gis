from flask import Flask, render_template
from db_utils import get_shelters

app = Flask(__name__)


@app.route('/')
def hello_world() -> object:
    shelters = get_shelters()

    return render_template('index.html', data=shelters)


if __name__ == '__main__':
    app.run()
