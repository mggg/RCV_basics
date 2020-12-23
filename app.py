import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from api_resources.PlackettLuceDirichlet import PlackettLuceDirichlet
from api_resources.BradleyTerryDirichlet import BradleyTerryDirichlet
from api_resources.AlternatingCrossover import AlternatingCrossover
from api_resources.CambridgeSampler import CambridgeSampler

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


api.add_resource(PlackettLuceDirichlet, '/' + os.path.join(API_BASE_URL, VERSION, 'plackettLuce'))
api.add_resource(BradleyTerryDirichlet, '/' + os.path.join(API_BASE_URL, VERSION, 'bradleyTerry'))
api.add_resource(AlternatingCrossover, '/' + os.path.join(API_BASE_URL, VERSION, 'alternatingCrossover'))
api.add_resource(CambridgeSampler, '/' + os.path.join(API_BASE_URL, VERSION, 'cambridgeSampler'))

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
