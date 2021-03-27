def add_dirichlet_arguments(parser):
    parser.add_argument('majMajAffinity', dest="majMajAffinity", required=True, type=float)
    parser.add_argument('majMinAffinity', dest="majMinAffinity", required=True, type=float)
    parser.add_argument('minMinAffinity', dest="minMinAffinity", required=True, type=float)
    parser.add_argument('minMajAffinity', dest="minMajAffinity", required=True, type=float)
