import pickle
import numpy as np
from pathlib import Path
from .helpers.VoterTypes import voting_agreement
from .helpers.TransferMethods import cincinnati_transfer
from .helpers.ElectionSimulations import rcv_run

DATA_DIR = './data'

# Load the ballot_type frequencies once into memory, used in the Cambridge model below
ballot_type_frequencies = pickle.load(Path(DATA_DIR, 'Cambridge_09to17_ballot_types.p').open('rb'))

# get ballot type frequencies, marginalized by the subset of interest
# white-first probabilities for each ballot variant
white_first_probs = {x: p for x, p in ballot_type_frequencies.items() if x[0] == 'W'}
sum_white_first_probs = sum(white_first_probs.values())
white_first_probs = {x: p/sum_white_first_probs for x, p in white_first_probs.items()}
white_first_ballot_types = list(white_first_probs.keys())
white_first_ballot_probs = list(white_first_probs.values())
# poc-first probabilities, for each ballot variant
poc_first_probs = {x: p for x, p in ballot_type_frequencies.items() if x[0] == 'C'}
sum_poc_first_probs = sum(poc_first_probs.values())
poc_first_probs = {x: p/sum_poc_first_probs for x, p in poc_first_probs.items()}
poc_first_ballot_types = list(poc_first_probs.keys())
poc_first_ballot_probs = list(poc_first_probs.values())


def _sample_ballots_for_voter_candidate_preference_group(max_ballot_length, pref_type_ballots, pref_type_probs, voter_candidate_orderings, num_samples, white_candidates, poc_candidates, voting_preferences):
    '''
    For each (voter_type x candidate_type) preference group, generate n_ballots many ballots based on a randomly sampled
    Cambridge ballot and the available candidates for each race
    '''
    candidate_orderings = {}
    white_white_pref, white_poc_pref, poc_poc_pref, poc_white_pref = voting_preferences

    if voter_candidate_orderings == 'white_voter_candidate_ordering':
        # define candidate preferences across voting groups
        candidate_orderings = {
            'W': (lambda: list(reversed(white_candidates))) if white_white_pref == voting_agreement['identical'] else (lambda: list(np.random.permutation(white_candidates))),
            'C': (lambda: list(reversed(poc_candidates))) if white_poc_pref == voting_agreement['identical'] else (lambda: list(np.random.permutation(poc_candidates)))
        }
    elif voter_candidate_orderings == 'poc_voter_candidate_ordering':
        candidate_orderings = {
            'W': (lambda: list(reversed(white_candidates))) if poc_white_pref == voting_agreement['identical'] else (lambda: list(np.random.permutation(white_candidates))),
            'C': (lambda: list(reversed(poc_candidates))) if poc_poc_pref == voting_agreement['identical'] else (lambda: list(np.random.permutation(poc_candidates)))
        }
    else:
        print('Cambridge Sampler, unrecognized voter candidate ordering: ', voter_candidate_orderings)

    selected_ballots = np.random.choice(
        pref_type_ballots,
        num_samples,
        p=pref_type_probs,
    )
    ballots_with_candidates = []
    for tuple_ballot in selected_ballots:
        selected_ballot = list(tuple_ballot)
        trimmed_selected_ballot = selected_ballot[:max_ballot_length]
        ballot_with_candidates = []
        w_ind = 0
        c_ind = 0
        for candidate_type in trimmed_selected_ballot:
            a = candidate_orderings[candidate_type]
            candidate_type_ordering = candidate_orderings[candidate_type]()
            relevant_ind = w_ind if candidate_type == 'W' else c_ind
            if (relevant_ind >= len(candidate_type_ordering)):
                break
            ballot_with_candidates.append(candidate_type_ordering[relevant_ind])
            if candidate_type == 'W':
                w_ind += 1
            else:
                c_ind += 1
        ballots_with_candidates.append(ballot_with_candidates)

    return ballots_with_candidates


def Cambridge_ballot_type_webapp(
    poc_share=0.33,
    poc_support_for_poc_candidates=0.7,
    poc_support_for_white_candidates=0.3,
    white_support_for_white_candidates=0.8,
    white_support_for_poc_candidates=0.2,
    num_ballots=1000,
    num_simulations=100,
    seats_open=4,
    num_poc_candidates=4,
    num_white_candidates=4,
    voting_preferences=[voting_agreement['identical'], voting_agreement['identical'], voting_agreement['identical'], voting_agreement['identical']],
    max_ballot_length=None,
    verbose=False
):
    # Cambridge Sampler Model
    # NOTE: This version of the function has been significantly refactored. Variable names may not always line up
    #       with the original version of this function, though an effort to synchronize them has been made.
    if max_ballot_length == None:
        max_ballot_length = num_poc_candidates+num_white_candidates
    poc_elected_Cambridge = []
    white_share = 1 - poc_share
    poc_candidates = ['A'+str(x) for x in range(num_poc_candidates)]
    white_candidates = ['B'+str(x) for x in range(num_white_candidates)]

    # Truncate the relevant ballots to reduce the statespace considered in sampling ballots
    # NOTE: Not all of these ballots are going to be valid, but this heuristic reduction in statespace
    #       has a measurable improvement on the sampling time when there num_candidates is reasonably small
    num_candidates = num_poc_candidates + num_white_candidates
    truncated_probs = {}
    for pref in set([x[:num_candidates] for x in white_first_ballot_types]):
        truncated_probs[pref] = sum(
            [white_first_probs[x] for x in white_first_probs if x[:num_candidates] == pref]
        )
    white_first_probs_truncated = truncated_probs
    truncated_probs = {}
    for pref in set([x[:num_candidates] for x in poc_first_ballot_types]):
        truncated_probs[pref] = sum(
            [poc_first_probs[x] for x in poc_first_probs if x[:num_candidates] == pref]
        )
    poc_first_probs_truncated = truncated_probs
    white_first_ballot_types_truncated = list(white_first_probs_truncated.keys())
    white_first_ballot_probs_truncated = list(white_first_probs_truncated.values())
    poc_first_ballot_types_truncated = list(poc_first_probs_truncated.keys())
    poc_first_ballot_probs_truncated = list(poc_first_probs_truncated.values())

    # Split the total number of ballots along the support lines
    num_white_white_voters = int(num_ballots*(white_share)*white_support_for_white_candidates)
    num_white_poc_voters = int(num_ballots*(white_share)*white_support_for_poc_candidates)
    num_poc_poc_voters = int(num_ballots*(poc_share)*poc_support_for_poc_candidates)
    num_poc_white_voters = int(num_ballots*(poc_share)*poc_support_for_white_candidates)

    while num_simulations > 0:
        ballots = []

        # white voters white-candidate first on ballot
        new_ballots = _sample_ballots_for_voter_candidate_preference_group(
            max_ballot_length,
            white_first_ballot_types_truncated,
            white_first_ballot_probs_truncated,
            'white_voter_candidate_ordering',
            num_white_white_voters,
            white_candidates,
            poc_candidates,
            voting_preferences
        )
        ballots.extend(new_ballots)
        # white voters poc first
        new_ballots = _sample_ballots_for_voter_candidate_preference_group(
            max_ballot_length,
            poc_first_ballot_types_truncated,
            poc_first_ballot_probs_truncated,
            'white_voter_candidate_ordering',
            num_white_poc_voters,
            white_candidates,
            poc_candidates,
            voting_preferences
        )
        ballots.extend(new_ballots)
        # poc voters poc first
        new_ballots = _sample_ballots_for_voter_candidate_preference_group(
            max_ballot_length,
            poc_first_ballot_types_truncated,
            poc_first_ballot_probs_truncated,
            'poc_voter_candidate_ordering',
            num_poc_poc_voters,
            white_candidates,
            poc_candidates,
            voting_preferences
        )
        ballots.extend(new_ballots)
        # poc voters white first
        new_ballots = _sample_ballots_for_voter_candidate_preference_group(
            max_ballot_length,
            white_first_ballot_types_truncated,
            white_first_ballot_probs_truncated,
            'poc_voter_candidate_ordering',
            num_poc_white_voters,
            white_candidates,
            poc_candidates,
            voting_preferences
        )
        ballots.extend(new_ballots)

        winners = rcv_run(
            ballots.copy(),
            poc_candidates + white_candidates,
            seats_open,
            cincinnati_transfer,
        )
        poc_elected_Cambridge.append(len([x for x in winners if x[0] == 'A']))
        num_simulations -= 1

    return poc_elected_Cambridge, None
