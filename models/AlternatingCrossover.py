import numpy as np
from .helpers.VoterTypes import voting_agreement
from .helpers.TransferMethods import cincinnati_transfer
from .helpers.ElectionSimulations import rcv_run


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
    verbose=False,
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
    while num_simulations > 0:
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
        winners = rcv_run(ac_ballots.copy(), white_candidates + poc_candidates, seats_open, cincinnati_transfer)
        poc_elected_ac.append(len([w for w in winners if w[0] == 'A']))
        num_simulations -= 1

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
