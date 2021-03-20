from models.helpers.VoterTypes import voting_agreement


def ballot_type_transform(args):
    ballot_types = [
        args['majMajCandidateAgreement'],
        args['majMinCandidateAgreement'],
        args['minMinCandidateAgreement'],
        args['minMajCandidateAgreement'],
    ]
    # Transform ballot_types
    int_ballot_types = [int(ty) for ty in ballot_types]
    unknown_types = [ty for ty in int_ballot_types if ty not in voting_agreement.values()]
    if len(unknown_types) > 0:
        print("WARNING : unknown types including" + unknown_types)
    return int_ballot_types
