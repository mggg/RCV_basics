from flask_restful import Resource, reqparse
from models import Alternating_crossover_webapp, bradley_terry_dirichlet, plackett_luce_dirichlet, Cambridge_ballot_type_webapp
from api.arguments.default_arguments import addCommonArguments
from api.transforms.default_transforms import (
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
from api.transforms.ballot_type_transforms import ballot_type_transform

# Arguments for the Ensemble resource
parser = reqparse.RequestParser()
addCommonArguments(parser)


class Ensemble(Resource):
    def get(self):
        args = parser.parse_args()
        ac_poc_elected_rcv, _ = Alternating_crossover_webapp(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        bt_poc_elected_rcv, _ = bradley_terry_dirichlet(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        pl_poc_elected_rcv, _ = plackett_luce_dirichlet(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        cs_poc_elected_rcv, _ = Cambridge_ballot_type_webapp(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        return dict(
            {
                'ac_poc_elected_rcv': ac_poc_elected_rcv,
                'bt_poc_elected_rcv': bt_poc_elected_rcv,
                'pl_poc_elected_rcv': pl_poc_elected_rcv,
                'cs_poc_elected_rcv': cs_poc_elected_rcv,
                'poc_elected_rcv': ac_poc_elected_rcv + bt_poc_elected_rcv + pl_poc_elected_rcv + cs_poc_elected_rcv,
                'seats_open': seats_open_transform(args)
            }
        )
