
def concentration_transform(args):
    # Transform all query parameter arguments from exponents to powers of two
    # concentrations = [poc_for_poc, poc_for_w, w_for_poc, w_for_w]
    concentration_exps = [
        args['minMinAffinity'],
        args['minMajAffinity'],
        args['majMinAffinity'],
        args['majMajAffinity'],
    ]
    return [ 2 ** exp for exp in concentration_exps]
