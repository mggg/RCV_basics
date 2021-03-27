from models.helpers.VoterTypes import voting_agreement


def fixed_ballot_type_transform(args):
    ballot_types = [
        args['majMajCandidateAgreement'],
        args['majMinCandidateAgreement'],
        args['minMinCandidateAgreement'],
        args['minMajCandidateAgreement'],
    ]
    # Transform ballot_types
    unknown_types = [ty for ty in ballot_types if ty not in voting_agreement.values()]
    if len(unknown_types) > 0:
        print("WARNING : unknown types including" + unknown_types)
    return ballot_types
