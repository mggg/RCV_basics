from flask_restful import Resource, reqparse
from model_details import luce_dirichlet
from common.param_transforms import (
    poc_share_transform,
    poc_support_for_poc_candidates_transform,
    poc_support_for_white_candidates_transform,
    white_support_for_white_candidates_transform,
    white_support_for_poc_candidates_transform,
    num_ballots_transform,
    seats_open_transform,
    num_white_candidates_transform,
    num_poc_candidates_transform,
    luce_concentration_transform,
    num_simulations_transform,
)


# Inputs for the LuceDirichlet resource
parser = reqparse.RequestParser()
parser.add_argument('seatsOpen', type=int, required=True)
parser.add_argument('ballots', required=True, type=int)
parser.add_argument('popMajParty', required=True, type=int)
parser.add_argument('majCandidates', required=True, type=int)
parser.add_argument('minCandidates', required=True, type=int)
parser.add_argument('percentageMajMajSupport', required=True, type=int)
parser.add_argument('percentageMinMinSupport', required=True, type=int)
parser.add_argument('numSimulations', required=True, type=int)
# all the Luce-concentration parameters
parser.add_argument('majMajAffinity', required=True, type=float)
parser.add_argument('majMinAffinity', required=True, type=float)
parser.add_argument('minMinAffinity', required=True, type=float)
parser.add_argument('minMajAffinity', required=True, type=float)



class LuceDirichlet(Resource):
    def get(self):
        args = parser.parse_args()
        print("poc_share: ", poc_share_transform(args))
        print("poc_support_for_poc_candidates: ", poc_support_for_poc_candidates_transform(args))
        print("poc_support_for_white_candidates: ", poc_support_for_white_candidates_transform(args))
        print("white_support_for_white_candidates: ", white_support_for_white_candidates_transform(args))
        print("white_support_for_poc_candidates: ", white_support_for_poc_candidates_transform(args))
        print("num_ballots: ", num_ballots_transform(args))
        print("seats_open: ", seats_open_transform(args))
        print("num_white_candidates: ", num_poc_candidates_transform(args))
        print("num_poc_candidates: ", num_white_candidates_transform(args))
        print("concentrations: ", luce_concentration_transform(args))
        print("num_simulations: ", num_simulations_transform(args))
        poc_elected_rcv, poc_at_large = luce_dirichlet(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            concentrations=luce_concentration_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        print("poc_at_large", poc_at_large)
        print("poc_elected_rcv", poc_elected_rcv)
        return dict({'poc_elected_rcv': poc_elected_rcv})
