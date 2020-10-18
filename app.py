from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from model_details import luce_dirichlet
import os

app = Flask(__name__)
api = Api(app)

API_BASE_URL = 'api'
VERSION = 'v1'
PORT = '1080'

# VARIABLES FOR RCV SIMULATION
# TODO: THESE NEED TO BE MADE INTO INPUT PARAMS FROM THE WEBFORM
##
poc_share = 0.30
poc_support_for_poc_candidates = 0.66
poc_support_for_white_candidates = 0.34
white_support_for_white_candidates = 1-1e-3
white_support_for_poc_candidates = 1e-3
num_ballots = 30
num_simulations = 1
seats_open = 6
num_poc_candidates = 6
num_white_candidates = 6
max_ballot_length = 6
# Luce model (Dirichlet variation)
concentrations = [0.5]*4  # >>1 means very similar supports, <<1 means most support goes to one or two candidates


parser = reqparse.RequestParser()
parser.add_argument('seatsOpen', type=int, required=True)
# TODO: ADD location once hooked up to a webform ,(location='form')

# Setting up CORS


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


class RCVSimulation(Resource):
    def get(self):
        args = parser.parse_args()
        print("args", args)
        poc_elected_rcv, poc_elected_atlarge = luce_dirichlet(
            poc_share=poc_share,
            poc_support_for_poc_candidates=poc_support_for_poc_candidates,
            poc_support_for_white_candidates=poc_support_for_white_candidates,
            white_support_for_white_candidates=white_support_for_white_candidates,
            white_support_for_poc_candidates=white_support_for_poc_candidates,
            num_ballots=num_ballots,
            num_simulations=num_simulations,
            seats_open=args['seatsOpen'],
            num_poc_candidates=num_poc_candidates,
            num_white_candidates=num_white_candidates,
            concentrations=concentrations
        )
        print("poc_elected_atlarge", poc_elected_atlarge)
        print("poc_elected_rcv", poc_elected_rcv)
        return dict({'results': poc_elected_rcv})


api.add_resource(RCVSimulation, '/' + os.path.join(API_BASE_URL, VERSION, 'simulate'))

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
