from models.helpers.VoterTypes import voting_agreement
# Translate unique codes to more_informative strings
models_codex = {
    0: 'pl',
    1: 'bt',
    2: 'ac',
    3: 'cs',
}


def models_to_simulate_transform(args):
    coded_models = args['modelsToSimulate']
    return [models_codex[model] for model in coded_models]


def concentration_transform(args):
    concentration_values = [
        args['majMinCandidateAgreement'],
        args['majMinCandidateAgreement'],
        args['majMinCandidateAgreement'],
        args['majMinCandidateAgreement'],
    ]
    # Expected range of incoming values: [0, 1]
    # Maps to: [1/2, 2]
    return [1/2 if val == 0 else 2 for val in concentration_values]


def fixed_ballot_type_transform(args):
    ballot_types = [
        args['majMajCandidateAgreement'],
        args['majMinCandidateAgreement'],
        args['minMinCandidateAgreement'],
        args['minMajCandidateAgreement'],
    ]
    # Transform ballot_types
    print("ballot_types", ballot_types)
    unknown_types = [ty for ty in ballot_types if ty not in voting_agreement.values()]
    if len(unknown_types) > 0:
        print("WARNING : unknown types including" + unknown_types)
    return ballot_types
