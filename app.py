import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from api.PlackettLuceDirichlet import PlackettLuceDirichlet
from api.BradleyTerryDirichlet import BradleyTerryDirichlet
from api.AlternatingCrossover import AlternatingCrossover
from api.CambridgeSampler import CambridgeSampler
from api.Ensemble import Ensemble

app = Flask(__name__)
app_api = Api(app)

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


app_api.add_resource(PlackettLuceDirichlet, '/' + os.path.join(API_BASE_URL, VERSION, 'plackettLuce'))
app_api.add_resource(BradleyTerryDirichlet, '/' + os.path.join(API_BASE_URL, VERSION, 'bradleyTerry'))
app_api.add_resource(AlternatingCrossover, '/' + os.path.join(API_BASE_URL, VERSION, 'alternatingCrossover'))
app_api.add_resource(CambridgeSampler, '/' + os.path.join(API_BASE_URL, VERSION, 'cambridgeSampler'))
app_api.add_resource(Ensemble, '/' + os.path.join(API_BASE_URL, VERSION, 'ensemble'))

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
