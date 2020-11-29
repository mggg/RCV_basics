from flask_restful import Resource, reqparse
from model_details import bradley_terry_dirichlet
from common.default_arguments import addCommonArguments
from common.default_transforms import (
    poc_share_transform,
    poc_support_for_poc_candidates_transform,
    poc_support_for_white_candidates_transform,
    white_support_for_white_candidates_transform,
    white_support_for_poc_candidates_transform,
    num_ballots_transform,
    seats_open_transform,
    num_white_candidates_transform,
    num_poc_candidates_transform,
    num_simulations_transform,
)
from common.dirichlet_transforms import concentration_transform

# Arguments for the BradleyTerryDirichlet resource
parser = reqparse.RequestParser()
addCommonArguments(parser)
parser.add_argument('majMajAffinity-bradleyTerry', dest="majMajAffinity", required=True, type=float)
parser.add_argument('majMinAffinity-bradleyTerry', dest="majMinAffinity", required=True, type=float)
parser.add_argument('minMinAffinity-bradleyTerry', dest="minMinAffinity", required=True, type=float)
parser.add_argument('minMajAffinity-bradleyTerry', dest="minMajAffinity", required=True, type=float)



class BradleyTerryDirichlet(Resource):
    def get(self):
        args = parser.parse_args()
        poc_elected_rcv, _ = bradley_terry_dirichlet(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            concentrations=concentration_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        return dict({'poc_elected_rcv': poc_elected_rcv})
