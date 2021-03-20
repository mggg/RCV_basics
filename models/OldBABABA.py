import random
from .helpers.TransferMethods import cincinnati_transfer
from .helpers.ElectionSimulations import rcv_run, at_large_run


def old_BABABA(
        poc_share=0.33,
        poc_support_for_poc_candidates=0.7,
        poc_support_for_white_candidates=0.3,
        white_support_for_white_candidates=0.8,
        white_support_for_poc_candidates=0.2,
        num_ballots=1000,
        num_simulations=100,
        seats_open=3,
        num_poc_candidates=2,
        num_white_candidates=3,
        scenarios_to_run=['A', 'B', 'C', 'D'],
        max_ballot_length=None,
        verbose=False):
    # Alternating Crossover Model
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    poc_candidates = [c for c in candidates if c[0] == 'A']
    white_candidates = [c for c in candidates if c[0] == 'B']

    def interleave(x, y):
        '''
        Interleaves two lists x and y
        '''
        x = list(x)
        y = list(y)
        minlength = min(len(x), len(y))
        return [z for pair in zip(x[:minlength], y[:minlength]) for z in pair]+x[minlength:]+y[minlength:]

    def white_bloc_ballots(scenario):
        if scenario in ['A', 'B']:
            return [white_candidates+poc_candidates]
        else:
            x = random.sample(white_candidates, len(white_candidates))
            y = random.sample(poc_candidates, len(poc_candidates))
            return [list(x) + list(y)]

    def white_cross_ballots(scenario):
        if scenario in ['A', 'B']:
            return [interleave(poc_candidates, white_candidates)]
        else:
            x = random.sample(white_candidates, len(white_candidates))
            y = random.sample(poc_candidates, len(poc_candidates))
            return [interleave(y, x)]

    def poc_bloc_ballots(scenario):
        if scenario in ['A', 'D']:
            return [poc_candidates+white_candidates]
        elif scenario == 'B':
            x = random.sample(white_candidates, len(white_candidates))
            y = random.sample(poc_candidates, len(poc_candidates))
            return [list(y)+white_candidates]
        else:
            x = random.sample(white_candidates, len(white_candidates))
            y = random.sample(poc_candidates, len(poc_candidates))
            return [list(y)+list(x)]

    def poc_cross_ballots(scenario):
        if scenario in ['A', 'D']:
            return [interleave(white_candidates, poc_candidates)]
        elif scenario == 'B':
            x = random.sample(white_candidates, len(white_candidates))
            y = random.sample(poc_candidates, len(poc_candidates))
            return [interleave(white_candidates, y)]
        else:
            x = random.sample(white_candidates, len(white_candidates))
            y = random.sample(poc_candidates, len(poc_candidates))
            return [interleave(x, y)]

    poc_elected_bababa = {}
    poc_elected_bababa_atlarge = {}
    for scenario in scenarios_to_run:
        poc_elected_bababa[scenario] = []
        poc_elected_bababa_atlarge[scenario] = []
        for n in range(num_simulations):
            babababallots = []
            # poc bloc
            a = int(num_ballots*poc_share*poc_support_for_poc_candidates)
            babababallots.extend([poc_bloc_ballots(scenario)[0][:max_ballot_length] for x in range(a)])
            # poc cross
            a = int(num_ballots*poc_share*poc_support_for_white_candidates)
            babababallots.extend([poc_cross_ballots(scenario)[0][:max_ballot_length] for x in range(a)])
            # white bloc
            a = int(num_ballots*(1-poc_share)*white_support_for_white_candidates)
            babababallots.extend([white_bloc_ballots(scenario)[0][:max_ballot_length] for x in range(a)])
            # white cross
            a = int(num_ballots*(1-poc_share)*white_support_for_poc_candidates)
            babababallots.extend([white_cross_ballots(scenario)[0][:max_ballot_length] for x in range(a)])

            if verbose:
                print(scenario)
                print(babababallots)

            # winners
            winners = rcv_run(babababallots.copy(), candidates, seats_open, cincinnati_transfer)
            poc_elected_bababa[scenario].append(len([w for w in winners if w[0] == 'A']))
            atlargewinners = at_large_run(babababallots.copy(), candidates, seats_open)
            poc_elected_bababa_atlarge[scenario].append(len([x for x in atlargewinners if x[0] == 'A']))
    return poc_elected_bababa, poc_elected_bababa_atlarge
