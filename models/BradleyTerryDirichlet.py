import numpy as np
from .helpers.BallotGenerators import paired_comparison_mcmc
from .helpers.TransferMethods import cincinnati_transfer
from .helpers.ElectionSimulations import rcv_run

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
        winners = rcv_run(ballots.copy(), candidates, seats_open, cincinnati_transfer)
        poc_elected.append(len([w for w in winners if w[0] == 'A']))

    return poc_elected, None
