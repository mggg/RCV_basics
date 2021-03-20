import pickle
import numpy as np
from pathlib import Path
from numpy.random import choice
from collections import defaultdict
from .helpers.TransferMethods import cincinnati_transfer
from .helpers.ElectionSimulations import rcv_run, at_large_run

DATA_DIR = './data'


def old_Cambridge_ballot_type(
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
    # Cambridge Sampler Model
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    num_candidates = [num_poc_candidates, num_white_candidates]
    poc_share = poc_share
    poc_elected_Cambridge = defaultdict(list)
    poc_elected_Cambridge_atlarge = defaultdict(list)
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]

    white_candidates = candidates[num_poc_candidates:]
    poc_candidates = candidates[:num_poc_candidates]

    # get ballot type frequencies
    ballot_type_frequencies = pickle.load(Path(DATA_DIR, 'Cambridge_09to17_ballot_types.p').open('rb'))
    white_first_probs = {x: p for x, p in ballot_type_frequencies.items() if x[0] == 'W'}
    poc_first_probs = {x: p for x, p in ballot_type_frequencies.items() if x[0] == 'C'}
    sum_white_first_probs = sum(white_first_probs.values())
    white_first_probs = {x: p/sum_white_first_probs for x, p in white_first_probs.items()}
    sum_poc_first_probs = sum(poc_first_probs.values())
    poc_first_probs = {x: p/sum_poc_first_probs for x, p in poc_first_probs.items()}

    # consolidate to only prefixes that are valid based on number of candidates
    consolidated_probs = {}
    for pref in set([x[:sum(num_candidates)] for x in white_first_probs.keys()]):
        consolidated_probs[pref] = sum(
            [white_first_probs[x] for x in white_first_probs if x[:sum(num_candidates)] == pref]
        )
    white_first_probs = consolidated_probs
    consolidated_probs = {}
    for pref in set([x[:sum(num_candidates)] for x in poc_first_probs.keys()]):
        consolidated_probs[pref] = sum(
            [poc_first_probs[x] for x in poc_first_probs if x[:sum(num_candidates)] == pref]
        )
    poc_first_probs = consolidated_probs

    for scenario in scenarios_to_run:
        for n in range(num_simulations):
            ballots = []

            # white voters white first
            for b in range(int(num_ballots*(1-poc_share)*white_support_for_white_candidates)):
                ballot_type = list(choice(
                    list(white_first_probs.keys()),
                    p=list(white_first_probs.values())
                ))[:max_ballot_length]
                ballot = []
                if scenario in ['C', 'D']:
                    candidate_ordering = {
                        'W': list(np.random.permutation(white_candidates)),
                        'C': list(np.random.permutation(poc_candidates))
                    }
                else:
                    candidate_ordering = {
                        'W': list(reversed(white_candidates)),
                        'C': list(reversed(poc_candidates))
                    }
                for j in range(len(ballot_type)):
                    if len(candidate_ordering[ballot_type[j]]) == 0:
                        break
                    else:
                        ballot.append(candidate_ordering[ballot_type[j]].pop())
                ballots.append(ballot[:max_ballot_length])

            # white voters poc first
            for b in range(int(num_ballots*(1-poc_share)*(white_support_for_poc_candidates))):
                ballot_type = list(choice(
                    list(poc_first_probs.keys()),
                    p=list(poc_first_probs.values())
                ))[:max_ballot_length]
                ballot = []
                if scenario in ['C', 'D']:
                    candidate_ordering = {
                        'W': list(np.random.permutation(white_candidates)),
                        'C': list(np.random.permutation(poc_candidates))
                    }
                else:
                    candidate_ordering = {
                        'W': list(reversed(white_candidates)),
                        'C': list(reversed(poc_candidates))
                    }
                for j in range(len(ballot_type)):
                    if len(candidate_ordering[ballot_type[j]]) == 0:
                        break
                    else:
                        ballot.append(candidate_ordering[ballot_type[j]].pop())
                ballots.append(ballot[:max_ballot_length])

            # poc voters poc first
            for b in range(int(num_ballots*(poc_share)*poc_support_for_poc_candidates)):
                ballot_type = list(choice(
                    list(poc_first_probs.keys()),
                    p=list(poc_first_probs.values())
                ))[:max_ballot_length]
                ballot = []
                if scenario in ['B']:
                    candidate_ordering = {
                        'W': list(reversed(white_candidates)),
                        'C': list(np.random.permutation(poc_candidates))
                    }
                elif scenario in ['C']:
                    candidate_ordering = {
                        'W': list(np.random.permutation(white_candidates)),
                        'C': list(np.random.permutation(poc_candidates))
                    }
                else:
                    candidate_ordering = {
                        'W': list(reversed(white_candidates)),
                        'C': list(reversed(poc_candidates))
                    }
                for j in range(len(ballot_type)):
                    if len(candidate_ordering[ballot_type[j]]) == 0:
                        break
                    else:
                        ballot.append(candidate_ordering[ballot_type[j]].pop())
                ballots.append(ballot[:max_ballot_length])

            # poc voters white first
            for b in range(int(num_ballots*(poc_share)*(poc_support_for_white_candidates))):
                ballot_type = list(choice(
                    list(white_first_probs.keys()),
                    p=list(white_first_probs.values())
                ))[:max_ballot_length]
                ballot = []
                if scenario in ['B']:
                    candidate_ordering = {
                        'W': list(reversed(white_candidates)),
                        'C': list(np.random.permutation(poc_candidates))
                    }
                elif scenario in ['C']:
                    candidate_ordering = {
                        'W': list(np.random.permutation(white_candidates)),
                        'C': list(np.random.permutation(poc_candidates))
                    }
                else:
                    candidate_ordering = {
                        'W': list(reversed(white_candidates)),
                        'C': list(reversed(poc_candidates))
                    }
                for j in range(len(ballot_type)):
                    if len(candidate_ordering[ballot_type[j]]) == 0:
                        break
                    else:
                        ballot.append(candidate_ordering[ballot_type[j]].pop())
                ballots.append(ballot[:max_ballot_length])
            winners = rcv_run(
                ballots.copy(),
                candidates,
                seats_open,
                cincinnati_transfer,
            )
            poc_elected_Cambridge[scenario].append(len([x for x in winners if x[0] == 'A']))

            atlargewinners = at_large_run(
                ballots.copy(),
                candidates,
                seats_open
            )
            poc_elected_Cambridge_atlarge[scenario].append(len([x for x in atlargewinners if x[0] == 'A']))
    return poc_elected_Cambridge, poc_elected_Cambridge_atlarge
