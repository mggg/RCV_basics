# Common arguments used across all resource endpoints
def add_default_arguments(parser):
    parser.add_argument('ballots', required=True, type=int)
    parser.add_argument('seatsOpen', type=int, required=True)
    parser.add_argument('majCandidates', required=True, type=int)
    parser.add_argument('minCandidates', required=True, type=int)
    parser.add_argument('popMajParty', required=True, type=int)
    parser.add_argument('percentageMajCohesion', required=True, type=int)
    parser.add_argument('percentageMinCohesion', required=True, type=int)
    parser.add_argument('numElectionsEachSimulation', required=True, type=int)
