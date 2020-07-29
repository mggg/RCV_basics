import pickle
from numpy.random import choice
from collections import defaultdict
import compute_winners as cw
import numpy as np
from itertools import permutations, product
import random
from vote_transfers import cincinnati_transfer

def Cambridge_ballot_type(
    poc_share = 0.33,
    poc_support_for_poc_candidates = 0.7,
    poc_support_for_white_candidates = 0.3,
    white_support_for_white_candidates = 0.8,
    white_support_for_poc_candidates = 0.2,
    num_ballots = 1000,
    num_simulations = 100,
    seats_open = 3,
    num_poc_candidates = 2,
    num_white_candidates = 3,
    scenarios_to_run = ['A', 'B', 'C', 'D']
):

    num_candidates = [num_poc_candidates, num_white_candidates]
    minority_share = poc_share
    preference_strengths = [white_support_for_white_candidates, poc_support_for_poc_candidates]
    num_seats = seats_open
    poc_elected_Cambridge = defaultdict(list)
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]

    white_candidates = candidates[num_candidates[0]:]
    poc_candidates = candidates[:num_candidates[0]]

    #get ballot type frequencies
    ballot_type_frequencies = pickle.load(open('Cambridge_09to17_ballot_types.p', 'rb'))
    white_first_probs = {x:p for x,p in ballot_type_frequencies.items() if x[0]=='W'}
    poc_first_probs = {x:p for x,p in ballot_type_frequencies.items() if x[0]=='C'}
    sum_white_first_probs = sum(white_first_probs.values())
    white_first_probs = {x:p/sum_white_first_probs for x,p in white_first_probs.items()}
    sum_poc_first_probs = sum(poc_first_probs.values())
    poc_first_probs = {x:p/sum_poc_first_probs for x,p in poc_first_probs.items()}

    #consolidate to only prefixes that are valid based on number of candidates
    consolidated_probs = {}
    for pref in set([x[:sum(num_candidates)] for x in white_first_probs.keys()]):
      consolidated_probs[pref] = sum(
          [white_first_probs[x] for x in white_first_probs if x[:sum(num_candidates)]==pref]
          )
    white_first_probs = consolidated_probs
    consolidated_probs = {}
    for pref in set([x[:sum(num_candidates)] for x in poc_first_probs.keys()]):
      consolidated_probs[pref] = sum(
          [poc_first_probs[x] for x in poc_first_probs if x[:sum(num_candidates)]==pref]
          )
    poc_first_probs = consolidated_probs

    for scenario in scenarios_to_run:
      print("\n", scenario)
      for n in range(num_simulations):
        print('.', end="")
        ballots = []
        ballot_length = len(candidates)

        #white voters white first
        for b in range(int(num_ballots*(1-minority_share)*preference_strengths[1])):
            ballot_type = list(choice(
                    list(white_first_probs.keys()),
                    p=list(white_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['C', 'D']:
                 candidate_ordering = {
                    'W':list(np.random.permutation(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)

        #white voters poc first
        for b in range(int(num_ballots*(1-minority_share)*(1-preference_strengths[1]))):
            ballot_type = list(choice(
                    list(poc_first_probs.keys()),
                    p=list(poc_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['C', 'D']:
                 candidate_ordering = {
                    'W':list(np.random.permutation(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)

        #poc voters poc first
        for b in range(int(num_ballots*(minority_share)*preference_strengths[0])):
            ballot_type = list(choice(
                    list(poc_first_probs.keys()),
                    p=list(poc_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['B']:
                 candidate_ordering = {
                    'W':list(reversed(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            elif scenario in ['C']:
                candidate_ordering = {
                   'W':list(np.random.permutation(white_candidates)),
                   'C':list(np.random.permutation(poc_candidates))
                }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)

        #poc voters white first
        for b in range(int(num_ballots*(minority_share)*(1-preference_strengths[0]))):
            ballot_type = list(choice(
                    list(white_first_probs.keys()),
                    p=list(white_first_probs.values())
            ))[:ballot_length]
            ballot = []
            if scenario in ['B']:
                 candidate_ordering = {
                    'W':list(reversed(white_candidates)),
                    'C':list(np.random.permutation(poc_candidates))
                 }
            elif scenario in ['C']:
                candidate_ordering = {
                   'W':list(np.random.permutation(white_candidates)),
                   'C':list(np.random.permutation(poc_candidates))
                }
            else:
                candidate_ordering = {
                   'W':list(reversed(white_candidates)),
                   'C':list(reversed(poc_candidates))
                }
            for j in range(len(ballot_type)):
                if len(candidate_ordering[ballot_type[j]])==0:
                    break
                else:
                    ballot.append(candidate_ordering[ballot_type[j]].pop())
            ballots.append(ballot)
        winners = cw.rcv_run(
            ballots.copy(),
            candidates,
            num_seats,
            cincinnati_transfer,
        )
        poc_elected_Cambridge[scenario].append(len([x for x in winners if x[0] == 'A']))
    return poc_elected_Cambridge


def BABABA(
    poc_share = 0.33,
    poc_support_for_poc_candidates = 0.7,
    poc_support_for_white_candidates = 0.3,
    white_support_for_white_candidates = 0.8,
    white_support_for_poc_candidates = 0.2,
    num_ballots = 1000,
    num_simulations = 100,
    seats_open = 3,
    num_poc_candidates = 2,
    num_white_candidates = 3,
    scenarios_to_run = ['A', 'B', 'C', 'D']
):
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    poc_candidates = [c for c in candidates if c[0]=='A']
    white_candidates = [c for c in candidates if c[0]=='B']

    def interleave(x,y):
        '''
        Interleaves two lists x and y
        '''
        x = list(x)
        y = list(y)
        minlength = min(len(x), len(y))
        return [z for pair in zip(x[:minlength],y[:minlength]) for z in pair]+x[minlength:]+y[minlength:]

    white_bloc_ballots = {
        'A':[white_candidates+poc_candidates],
        'B':[white_candidates+poc_candidates],
        'C':[list(x)+list(y) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[list(x)+list(y) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))]
    }
    white_cross_ballots = {
        'A':[interleave(poc_candidates, white_candidates)],
        'B':[interleave(poc_candidates, white_candidates)],
        'C':[interleave(y,x) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[interleave(y,x) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))]
    }
    poc_bloc_ballots = {
        'A':[poc_candidates+white_candidates],
        'B':[list(x)+white_candidates for x in list(permutations(poc_candidates))],
        'C':[list(y)+list(x) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[poc_candidates+white_candidates],
    }
    poc_cross_ballots = {
        'A':[interleave(white_candidates, poc_candidates)],
        'B':[interleave(white_candidates,x) for x in list(permutations(poc_candidates))],
        'C':[interleave(x,y) for x,y in product(list(permutations(white_candidates)), list(permutations(poc_candidates)))],
        'D':[interleave(white_candidates, poc_candidates)],
    }

    poc_elected_bababa = {}
    for scenario in scenarios_to_run:
      poc_elected_bababa[scenario] = []
      for n in range(num_simulations):
        babababallots = []
        #poc bloc
        a = int(num_ballots*poc_share*poc_support_for_poc_candidates)
        babababallots.extend(random.choices(poc_bloc_ballots[scenario],k=a))
        #poc cross
        a = int(num_ballots*poc_share*poc_support_for_white_candidates)
        babababallots.extend(random.choices(poc_cross_ballots[scenario],k=a))
        #white bloc
        a = int(num_ballots*(1-poc_share)*white_support_for_white_candidates)
        babababallots.extend(random.choices(white_bloc_ballots[scenario],k=a))
        #white cross
        a = int(num_ballots*(1-poc_share)*white_support_for_poc_candidates)
        babababallots.extend(random.choices(white_cross_ballots[scenario],k=a))
        #winners
        winners = cw.rcv_run(babababallots, candidates, seats_open, cincinnati_transfer)
        poc_elected_bababa[scenario].append(len([w for w in winners if w[0]=='A']))
    return poc_elected_bababa
