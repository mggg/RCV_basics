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
  return args['numElectionsEachSimulation']

def seats_open_transform(args):
  return args['seatsOpen']

def num_poc_candidates_transform(args):
  return args['majCandidates']

def num_white_candidates_transform(args):
  return args['minCandidates']
