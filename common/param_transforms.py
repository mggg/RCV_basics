def poc_share_transform(args):
  value = args['popMajParty']
  return 1 - float(value / 100)

def poc_support_for_poc_candidates_transform(args):
  value = args['percentageMinMinSupport']
  return float(value / 100)

def poc_support_for_white_candidates_transform(args):
  value = args['percentageMinMinSupport']
  return 1.0 - float(value / 100)

def white_support_for_white_candidates_transform(args):
  value = args['percentageMajMajSupport']
  return float(value / 100)

def white_support_for_poc_candidates_transform(args):
  value = args['percentageMajMajSupport']
  return 1.0  - float(value / 100)

def num_ballots_transform(args):
  return args['ballots']

def num_simulations_transform(args):
  return args['numSimulations']

def seats_open_transform(args):
  return args['seatsOpen']

def num_poc_candidates_transform(args):
  return args['majCandidates']

def num_white_candidates_transform(args):
  return args['minCandidates']

def luce_concentration_transform(args):
    # Transform all query parameter arguments from exponents to powers of two
    # concentrations = [poc_for_poc, poc_for_w, w_for_poc, w_for_w]
    concentration_exps = [
        args['minMinAffinity'],
        args['minMajAffinity'],
        args['majMinAffinity'],
        args['majMajAffinity'],
    ]
    return [ 2 ** exp for exp in concentration_exps]

# poc_share = 0.30
# poc_support_for_poc_candidates = 0.66
# poc_support_for_white_candidates = 0.34
# white_support_for_white_candidates = 1-1e-3
# white_support_for_poc_candidates = 1e-3
# num_ballots = 30
# seats_open = 6
# num_poc_candidates = 6
# num_white_candidates = 6
# max_ballot_length = 6
