def ballot_type_transform(args):
    ballot_types = [
        args['majMajCandidateAgreement'],
        args['majMinCandidateAgreement'],
        args['minMinCandidateAgreement'],
        args['minMajCandidateAgreement'],
    ]
    print(ballot_types)
    print([bool(type) for types in ballot_types])
    # Transform ballot_types
    return [bool(type) for types in ballot_types]
