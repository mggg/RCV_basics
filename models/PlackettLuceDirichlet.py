import numpy as np
from .helpers.BallotGenerators import paired_comparison_mcmc
from .helpers.TransferMethods import cincinnati_transfer
from .helpers.ElectionSimulations import rcv_run


def _sum_to_one(list_of_vectors):
    '''
    Fixes small errors in place to make sure vectors sum to 1
    '''
    for v in list_of_vectors:
        n = np.argmax(v)  # fix highest value
        v[n] = 1-sum([x for i, x in enumerate(v) if i != n])


def plackett_luce_dirichlet(
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
    while num_simulations > 0:
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
        _sum_to_one([white_voter_support_vector, poc_voter_support_vector])
        possible_candidate_races = list(race_of_candidate.keys())
        # white
        for i in range(int(numballots*(1-poc_share))):
            ballots.append(
                np.random.choice(possible_candidate_races, size=len(race_of_candidate), p=white_voter_support_vector, replace=False)
            )
        # poc
        for i in range(int(numballots*poc_share)):
            ballots.append(
                np.random.choice(possible_candidate_races, size=len(race_of_candidate), p=poc_voter_support_vector, replace=False)
            )
        # winners
        ballots = [b[:max_ballot_length] for b in ballots]
        winners = rcv_run(ballots.copy(), candidates, seats_open, cincinnati_transfer)
        poc_elected_luce.append(len([w for w in winners if w[0] == 'A']))
        num_simulations -= 1

    return poc_elected_luce, None
