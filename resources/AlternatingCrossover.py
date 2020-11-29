from flask_restful import Resource, reqparse
from model_details import BABABA
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
from common.ballot_type_transforms import ballot_type_transform

# Arguments for the AlternatingCrossover resource
parser = reqparse.RequestParser()
addCommonArguments(parser)
parser.add_argument('majMajCandidateAgreement-alternatingCrossover', dest="majMajCandidateAgreement", required=True, type=float)
parser.add_argument('majMinCandidateAgreement-alternatingCrossover', dest="majMinCandidateAgreement", required=True, type=float)
parser.add_argument('minMinCandidateAgreement-alternatingCrossover', dest="minMinCandidateAgreement", required=True, type=float)
parser.add_argument('minMajCandidateAgreement-alternatingCrossover', dest="minMajCandidateAgreement", required=True, type=float)



class AlternatingCrossover(Resource):
    def get(self):
        args = parser.parse_args()
        poc_elected_rcv, _ = BABABA(
            poc_share=poc_share_transform(args),
            poc_support_for_poc_candidates=poc_support_for_poc_candidates_transform(args),
            poc_support_for_white_candidates=poc_support_for_white_candidates_transform(args),
            white_support_for_white_candidates=white_support_for_white_candidates_transform(args),
            white_support_for_poc_candidates=white_support_for_poc_candidates_transform(args),
            num_ballots=num_ballots_transform(args),
            seats_open=seats_open_transform(args),
            num_white_candidates=num_poc_candidates_transform(args),
            num_poc_candidates=num_white_candidates_transform(args),
            scenarios_to_run=ballot_type_transform(args),
            num_simulations=num_simulations_transform(args),
        )
        return dict({'poc_elected_rcv': poc_elected_rcv})
