def add_ensemble_arguments(parser):
    parser.add_argument('modelsToSimulate', dest="modelsToSimulate", required=True, type=int, action='append')
    parser.add_argument('majMajCandidateAgreement', dest="majMajCandidateAgreement", required=True, type=int)
    parser.add_argument('majMinCandidateAgreement', dest="majMinCandidateAgreement", required=True, type=int)
    parser.add_argument('minMinCandidateAgreement', dest="minMinCandidateAgreement", required=True, type=int)
    parser.add_argument('minMajCandidateAgreement', dest="minMajCandidateAgreement", required=True, type=int)
