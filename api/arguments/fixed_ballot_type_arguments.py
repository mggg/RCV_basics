
def add_fixed_ballot_type_arguments(parser):
    parser.add_argument('majMajCandidateAgreement', dest="majMajCandidateAgreement", required=True, type=int)
    parser.add_argument('majMinCandidateAgreement', dest="majMinCandidateAgreement", required=True, type=int)
    parser.add_argument('minMinCandidateAgreement', dest="minMinCandidateAgreement", required=True, type=int)
    parser.add_argument('minMajCandidateAgreement', dest="minMajCandidateAgreement", required=True, type=int)
