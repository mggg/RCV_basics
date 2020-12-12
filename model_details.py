import pickle
from numpy.random import choice
from collections import defaultdict
import compute_winners as cw
import numpy as np
from itertools import permutations, product
import random
from vote_transfers import cincinnati_transfer
from ballot_generators import paired_comparison_mcmc
from pathlib import Path

DATA_DIR = './data'


def sum_to_one(list_of_vectors):
    '''
    Fixes small errors in place to make sure vectors sum to 1
    '''
    for v in list_of_vectors:
        n = np.argmax(v)  # fix highest value
        v[n] = 1-sum([x for i, x in enumerate(v) if i != n])


def Cambridge_ballot_type(
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
            winners = cw.rcv_run(
                ballots.copy(),
                candidates,
                seats_open,
                cincinnati_transfer,
            )
            poc_elected_Cambridge[scenario].append(len([x for x in winners if x[0] == 'A']))

            atlargewinners = cw.at_large_run(
                ballots.copy(),
                candidates,
                seats_open
            )
            poc_elected_Cambridge_atlarge[scenario].append(len([x for x in atlargewinners if x[0] == 'A']))
    return poc_elected_Cambridge, poc_elected_Cambridge_atlarge


def BABABA(
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
    verbose=False
):
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
            winners = cw.rcv_run(babababallots.copy(), candidates, seats_open, cincinnati_transfer)
            poc_elected_bababa[scenario].append(len([w for w in winners if w[0] == 'A']))
            atlargewinners = cw.at_large_run(babababallots.copy(), candidates, seats_open)
            poc_elected_bababa_atlarge[scenario].append(len([x for x in atlargewinners if x[0] == 'A']))
    return poc_elected_bababa, poc_elected_bababa_atlarge


def luce_dirichlet(
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
        concentrations=[1.0, 1.0, 1.0, 1.0],  # poc_for_poc, poc_for_w, w_for_poc, w_for_w.
        max_ballot_length=None):
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    # alphas = poc_for_poc, poc_for_w, w_for_poc, w_for_w.
    alphas = concentrations
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    race_of_candidate = {x: x[0] for x in candidates}

    # simulate
    poc_elected_luce = []
    poc_elected_luce_atlarge = []
    for n in range(num_simulations):
        # get support vectors
        noise_poc_voters = list(np.random.dirichlet([alphas[0]]*num_poc_candidates))+list(np.random.dirichlet([alphas[1]]*num_white_candidates))
        noise_white_voters = list(np.random.dirichlet([alphas[2]]*num_poc_candidates))+list(np.random.dirichlet([alphas[3]]*num_white_candidates))
        poc_voter_support_vector = []
        white_voter_support_vector = []
        # For each candidate, deetermine their support based on their race
        for i, (c, r) in enumerate(race_of_candidate.items()):
            # For POC candidates
            if r == 'A':
                white_voter_support_vector.append((white_support_for_poc_candidates*noise_white_voters[i]))
                poc_voter_support_vector.append((poc_support_for_poc_candidates*noise_poc_voters[i]))
            # For White candidates
            elif r == 'B':
                white_voter_support_vector.append((white_support_for_white_candidates*noise_white_voters[i]))
                poc_voter_support_vector.append((poc_support_for_white_candidates*noise_poc_voters[i]))
        ballots = []
        numballots = num_ballots
        sum_to_one([white_voter_support_vector, poc_voter_support_vector])
        # white
        for i in range(int(numballots*(1-poc_share))):
            ballots.append(
                np.random.choice(list(race_of_candidate.keys()), size=len(race_of_candidate), p=white_voter_support_vector, replace=False)
            )
        # poc
        for i in range(int(numballots*poc_share)):
            ballots.append(
                np.random.choice(list(race_of_candidate.keys()), size=len(race_of_candidate), p=poc_voter_support_vector, replace=False)
            )
        # winners
        ballots = [b[:max_ballot_length] for b in ballots]
        winners = cw.rcv_run(ballots.copy(), candidates, seats_open, cincinnati_transfer)
        poc_elected_luce.append(len([w for w in winners if w[0] == 'A']))
        atlargewinners = cw.at_large_run(ballots.copy(), candidates, seats_open)
        poc_elected_luce_atlarge.append(len([x for x in atlargewinners if x[0] == 'A']))

    return poc_elected_luce, poc_elected_luce_atlarge


def bradley_terry_dirichlet(
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
        concentrations=[1.0, 1.0, 1.0, 1.0],  # poc_for_poc, poc_for_w, w_for_poc, w_for_w
        max_ballot_length=None):
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    num_candidates = [num_poc_candidates, num_white_candidates]
    alphas = concentrations
    candidates = ['A'+str(x) for x in range(num_poc_candidates)]+['B'+str(x) for x in range(num_white_candidates)]
    race_of_candidate = {x: x[0] for x in candidates}

    # simulate
    poc_elected = []
    poc_elected_atlarge = []
    for n in range(num_simulations):
        # get support vectors
        noise0 = list(np.random.dirichlet([alphas[0]]*num_poc_candidates))+list(np.random.dirichlet([alphas[1]]*num_white_candidates))
        noise1 = list(np.random.dirichlet([alphas[2]]*num_poc_candidates))+list(np.random.dirichlet([alphas[3]]*num_white_candidates))
        white_voter_support_vector = []
        poc_voter_support_vector = []
        for i, (c, r) in enumerate(race_of_candidate.items()):
            if r == 'A':
                white_voter_support_vector.append((white_support_for_poc_candidates*noise1[i]))
                poc_voter_support_vector.append((poc_support_for_poc_candidates*noise0[i]))
            elif r == 'B':
                white_voter_support_vector.append((white_support_for_white_candidates*noise1[i]))
                poc_voter_support_vector.append((poc_support_for_white_candidates*noise0[i]))

        ballots = []
        numballots = num_ballots
        ballots = paired_comparison_mcmc(
            num_ballots,
            {
                0: {x: poc_voter_support_vector[i] for i, x in enumerate(candidates)},
                1: {x: white_voter_support_vector[i] for i, x in enumerate(candidates)}
            },
            None,
            candidates,
            {0: poc_share, 1: 1-poc_share},
            [0, 1],
            sample_interval=10,
            verbose=False
        )
        # winners
        ballots = [b[:max_ballot_length] for b in ballots]
        winners = cw.rcv_run(ballots.copy(), candidates, seats_open, cincinnati_transfer)
        poc_elected.append(len([w for w in winners if w[0] == 'A']))
        atlargewinners = cw.at_large_run(ballots.copy(), candidates, seats_open)
        poc_elected_atlarge.append(len([x for x in atlargewinners if x[0] == 'A']))

    return poc_elected, poc_elected_atlarge


# An enum to define possible voter preferences for a voting group towards a candidate group
# Identical - all voters from that group have the same preference for a candidate group
# Random - each voter from that group has a randomly selected preference for a candidate group
voting_agreement = {
    'random': 0,
    'identical': 1,
}

#######################################
#######################################
# Cambridge Sampler Specific variables
# and functions
#######################################

# Load the ballot_type frequencies once into memory, used in the Cambridge model below
ballot_type_frequencies = pickle.load(Path(DATA_DIR, 'Cambridge_09to17_ballot_types.p').open('rb'))

# get ballot type frequencies, marginalized by the subset of interest
# white-first probabilities for each ballot variant
white_first_probs = {x: p for x, p in ballot_type_frequencies.items() if x[0] == 'W'}
sum_white_first_probs = sum(white_first_probs.values())
white_first_probs = {x: p/sum_white_first_probs for x, p in white_first_probs.items()}
# poc-first probabilities, for each ballot variant
poc_first_probs = {x: p for x, p in ballot_type_frequencies.items() if x[0] == 'C'}
sum_poc_first_probs = sum(poc_first_probs.values())
poc_first_probs = {x: p/sum_poc_first_probs for x, p in poc_first_probs.items()}


def sample_ballots_for_voter_candidate_preference_group(n_ballots, max_ballot_length, pref_type_ballots_and_probs, voter_candidate_orderings):
    '''
    For each (voter_type x candidate_type) preference group, generate n_ballots many ballots based on a randomly sampled
    Cambridge ballot and the available candidates for each race
    '''
    sampled_ballots = []
    for b in range(n_ballots):
        selected_ballot = list(choice(
            list(pref_type_ballots_and_probs.keys()),
            p=list(pref_type_ballots_and_probs.values())
        ))
        trimmed_selected_ballot = selected_ballot[:max_ballot_length]
        ballot_with_candidates = []
        w_ind = 0
        c_ind = 0
        for candidate_type in trimmed_selected_ballot:
            candidate_type_ordering = voter_candidate_orderings[candidate_type]
            relevant_ind = w_ind if candidate_type == 'W' else c_ind
            if (relevant_ind >= len(candidate_type_ordering)):
                break
            ballot_with_candidates.append(candidate_type_ordering[relevant_ind])
            if candidate_type == 'W':
                w_ind += 1
            else:
                c_ind += 1

        sampled_ballots.append(ballot_with_candidates)
    return sampled_ballots


def Cambridge_ballot_type_webapp(
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
        voting_preferences=[voting_agreement['identical'], voting_agreement['identical'], voting_agreement['identical'], voting_agreement['identical']],
        max_ballot_length=None,
        verbose=False):
    # Cambridge Sampler Model
    # NOTE: This version of the function has been significantly refactored. Variable names may not always line up
    #       with the original version of this function, though an effort to synchronize them has been made.
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    num_candidates = num_poc_candidates + num_white_candidates
    poc_elected_Cambridge = []
    white_share = 1 - poc_share
    white_white_pref, white_poc_pref, poc_poc_pref, poc_white_pref = voting_preferences
    poc_candidates = ['A'+str(x) for x in range(num_poc_candidates)]
    white_candidates = ['B'+str(x) for x in range(num_white_candidates)]

    # consolidate to only prefixes that are valid based on number of candidates
    # I.e.: shorten and aggregate all ballots that have too many candidate
    # for white candidates
    consolidated_probs = {}
    for shortened_ballot in set([x[:num_candidates] for x in white_first_probs.keys()]):
        consolidated_probs[shortened_ballot] = sum(
            [white_first_probs[x] for x in white_first_probs if x[:num_candidates] == shortened_ballot]
        )
    consolidated_white_first_probs = consolidated_probs
    # for poc candidates
    consolidated_probs = {}
    for shortened_ballot in set([x[:num_candidates] for x in poc_first_probs.keys()]):
        consolidated_probs[shortened_ballot] = sum(
            [poc_first_probs[x] for x in poc_first_probs if x[:num_candidates] == shortened_ballot]
        )
    consolidated_poc_first_probs = consolidated_probs

    # Split the total number of ballots along the support lines
    num_white_white_voters = int(num_ballots*(white_share)*white_support_for_white_candidates)
    num_white_poc_voters = int(num_ballots*(white_share)*white_support_for_poc_candidates)
    num_poc_poc_voters = int(num_ballots*(poc_share)*poc_support_for_poc_candidates)
    num_poc_white_voters = int(num_ballots*(poc_share)*poc_support_for_white_candidates)

    # define candidate preferences across voting groups
    white_voter_candidate_ordering = {
        'W': list(reversed(white_candidates) if white_white_pref == voting_agreement['identical'] else np.random.permutation(white_candidates)),
        'C': list(reversed(poc_candidates) if white_poc_pref == voting_agreement['identical'] else np.random.permutation(poc_candidates))
    }
    poc_voter_candidate_ordering = {
        'W': list(reversed(white_candidates) if poc_white_pref == voting_agreement['identical'] else np.random.permutation(white_candidates)),
        'C': list(reversed(poc_candidates) if poc_poc_pref == voting_agreement['identical'] else np.random.permutation(poc_candidates))
    }

    for n in range(num_simulations):
        ballots = []

        # white voters white-candidate first on ballot
        ballots += sample_ballots_for_voter_candidate_preference_group(num_white_white_voters, max_ballot_length, consolidated_white_first_probs, white_voter_candidate_ordering)
        # white voters poc first
        ballots += sample_ballots_for_voter_candidate_preference_group(num_white_poc_voters, max_ballot_length, consolidated_poc_first_probs, white_voter_candidate_ordering)
        # poc voters poc first
        ballots += sample_ballots_for_voter_candidate_preference_group(num_poc_poc_voters, max_ballot_length, consolidated_poc_first_probs, poc_voter_candidate_ordering)
        # poc voters white first
        ballots += sample_ballots_for_voter_candidate_preference_group(num_poc_white_voters, max_ballot_length, consolidated_white_first_probs, poc_voter_candidate_ordering)

        winners = cw.rcv_run(
            ballots.copy(),
            poc_candidates + white_candidates,
            seats_open,
            cincinnati_transfer,
        )
        poc_elected_Cambridge.append(len([x for x in winners if x[0] == 'A']))

    return poc_elected_Cambridge, None


def Alternating_crossover_webapp(
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
    voting_preferences=[voting_agreement['identical'], voting_agreement['identical'], voting_agreement['identical'], voting_agreement['identical']],
    max_ballot_length=None,
    verbose=False
):
    # Alternating Crossover Model, adapted from the BABABA model above
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    white_candidates = ['B'+str(x) for x in range(num_white_candidates)]
    poc_candidates = ['A'+str(x) for x in range(num_poc_candidates)]
    white_share = 1 - poc_share
    # white_bloc_pref, white_cross_pref, poc_bloc_pref, poc_cross_pref = voting_preferences
    white_white_pref, white_poc_pref, poc_poc_pref, poc_white_pref = voting_preferences

    poc_elected_ac = []
    num_white_bloc_voters = int(num_ballots*(white_share)*white_support_for_white_candidates)
    num_white_cross_voters = int(num_ballots*(white_share)*white_support_for_poc_candidates)
    num_poc_bloc_voters = int(num_ballots*(poc_share)*poc_support_for_poc_candidates)
    num_poc_cross_voters = int(num_ballots*(poc_share)*poc_support_for_white_candidates)
    for n in range(num_simulations):
        ac_ballots = []
        # white bloc
        ac_ballots.extend(
            [bloc_ballots(white_white_pref, white_candidates, white_poc_pref, poc_candidates)[:max_ballot_length] for x in range(num_white_bloc_voters)]
        )
        # white cross
        ac_ballots.extend(
            [cross_ballots(white_white_pref, white_candidates, white_poc_pref, poc_candidates)[:max_ballot_length] for x in range(num_white_cross_voters)]
        )
        # poc bloc
        ac_ballots.extend(
            [bloc_ballots(poc_poc_pref, poc_candidates, poc_white_pref, white_candidates)[:max_ballot_length] for x in range(num_poc_bloc_voters)]
        )
        # poc cross
        ac_ballots.extend(
            [cross_ballots(poc_poc_pref, poc_candidates, poc_white_pref, white_candidates)[:max_ballot_length] for x in range(num_poc_cross_voters)]
        )

        if verbose:
            print(ac_ballots)

        # winners
        winners = cw.rcv_run(ac_ballots.copy(), white_candidates + poc_candidates, seats_open, cincinnati_transfer)
        poc_elected_ac.append(len([w for w in winners if w[0] == 'A']))

    return poc_elected_ac, None


def interleave(x, y):
    '''
    Interleaves two lists x and y
    '''
    x = list(x)
    y = list(y)
    minlength = min(len(x), len(y))
    return [z for pair in zip(x[:minlength], y[:minlength]) for z in pair]+x[minlength:]+y[minlength:]


def bloc_ballots(same_group_pref, same_group_candidates, opposite_group_pref, opposite_group_candidates):
    same_group_candidates_order = same_group_candidates if same_group_pref == voting_agreement['identical'] else list(np.random.permutation(same_group_candidates))
    opposite_group_candidates_order = opposite_group_candidates if opposite_group_pref == voting_agreement['identical'] else list(np.random.permutation(opposite_group_candidates))
    return same_group_candidates_order + opposite_group_candidates_order


def cross_ballots(same_group_pref, same_group_candidates, opposite_group_pref, opposite_group_candidates):
    cross_opposite_group_candidates = opposite_group_candidates if opposite_group_pref == voting_agreement['identical'] else list(np.random.permutation(opposite_group_candidates))
    cross_same_group_candidates = same_group_candidates if same_group_pref == voting_agreement['identical'] else list(np.random.permutation(same_group_candidates))
    return interleave(cross_opposite_group_candidates, cross_same_group_candidates)
