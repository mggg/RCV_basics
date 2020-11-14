import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from resources.LuceDirichlet import LuceDirichlet

app = Flask(__name__)
api = Api(app)

API_BASE_URL = 'api'
VERSION = 'v1'
PORT = '1080'


@app.after_request
def add_headers(response):
    # Setting up CORS
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


api.add_resource(LuceDirichlet, '/' + os.path.join(API_BASE_URL, VERSION, 'simulate'))
# api.add_resource(RCVSimulation, '/' + os.path.join(API_BASE_URL, VERSION, 'simulate'))
# api.add_resource(RCVSimulation, '/' + os.path.join(API_BASE_URL, VERSION, 'simulate'))
# api.add_resource(RCVSimulation, '/' + os.path.join(API_BASE_URL, VERSION, 'simulate'))

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
