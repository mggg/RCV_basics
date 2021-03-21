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
