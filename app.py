from flask import Flask

from job51_spider import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/job/<input_job>/<qry_pages>')
def search_51_job(input_job, qry_pages):
    return search_job(input_job, qry_pages)


if __name__ == '__main__':
    app.run()
