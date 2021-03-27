
def concentration_transform(args):
    # Transform all query parameter arguments from exponents to powers of two
    # concentrations = [poc_for_poc, poc_for_w, w_for_poc, w_for_w]
    concentration_exps = [
        args['minMinAffinity'],
        args['minMajAffinity'],
        args['majMinAffinity'],
        args['majMajAffinity'],
    ]
    # Expected range of incoming values: [-1, -0.5, 0, 0.5, 1]
    # Maps to: [1/2, ..., 2]
    return [2 ** exp for exp in concentration_exps]
