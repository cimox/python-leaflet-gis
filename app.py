from flask import Flask

app = Flask(__name__)


@app.route('/', defaults={'name': 'John'})
@app.route('/<string:name>/')
def hello_world(name: str) -> str:
    return 'Hello {}!'.format(name)


if __name__ == '__main__':
    app.run()
