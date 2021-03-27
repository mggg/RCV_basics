from flask_restful import Resource, reqparse
from models import Alternating_crossover_webapp, bradley_terry_dirichlet, plackett_luce_dirichlet, Cambridge_ballot_type_webapp
from api.arguments.default_arguments import add_default_arguments
from api.arguments.ensemble_arguments import add_ensemble_arguments
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
from api.transforms.ensemble_transforms import (
    models_to_simulate_transform,
    fixed_ballot_type_transform,
    concentration_transform,
)

# Arguments for the Ensemble resource
parser = reqparse.RequestParser()
add_default_arguments(parser)
add_ensemble_arguments(parser)


def run_simulation_by_type(args, model_type):
    poc_elected_rcv = []
    if model_type == 'ac':
        poc_elected_rcv, _ = Alternating_crossover_webapp(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            voting_preferences=fixed_ballot_type_transform(args),
            num_simulations=1
        )
    if model_type == 'bt':
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
            num_simulations=1
        )
    if model_type == 'pl':
        poc_elected_rcv, _ = plackett_luce_dirichlet(
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
            num_simulations=1
        )
    if model_type == 'cs':
        poc_elected_rcv, _ = Cambridge_ballot_type_webapp(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            voting_preferences=fixed_ballot_type_transform(args),
            num_simulations=1
        )
    return poc_elected_rcv


class Ensemble(Resource):
    def get(self):
        args = parser.parse_args()
        # For each simulation, iterate over the possible model types to get a close-to-even distribution of each model_type
        models = models_to_simulate_transform(args)
        num_simulations = num_simulations_transform(args)
        ac_poc_elected_rcv, bt_poc_elected_rcv, pl_poc_elected_rcv, cs_poc_elected_rcv = [], [], [], []
        if len(models) == 0:
            return {}
        num_possible_models = len(models)
        for i in range(num_simulations):
            model_type = models[i % num_possible_models]
            poc_elected = run_simulation_by_type(args, model_type)
            if model_type == 'ac':
                ac_poc_elected_rcv += poc_elected
            if model_type == 'bt':
                bt_poc_elected_rcv += poc_elected
            if model_type == 'pl':
                pl_poc_elected_rcv += poc_elected
            if model_type == 'cs':
                cs_poc_elected_rcv += poc_elected

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
