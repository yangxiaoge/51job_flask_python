from flask import Flask

from job51_spider import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/job/<input_job>')
def search_51_job(input_job):
    return search_job(input_job)


if __name__ == '__main__':
    app.run()
