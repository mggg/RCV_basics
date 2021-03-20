import random


def _remove_cand(cand, ballot_list):
    for n, ballot in enumerate(ballot_list):
        new_ballot = []
        for c in ballot:
            if c != cand:
                new_ballot.append(c)
        ballot_list[n] = new_ballot


def cincinnati_transfer(cand, ballot_list, win_lose, cutoff):
    if win_lose == 'lose':
        _remove_cand(cand, ballot_list)
    else:
        cand_ballots_index = []
        single_cand_ballots_index = []
        for n, ballot in enumerate(ballot_list):
            if ballot[0] == cand and len(ballot) == 1:
                single_cand_ballots_index.append(n)
            elif ballot[0] == cand and len(ballot) > 1:
                cand_ballots_index.append(n)

        rand_winners1 = random.sample(single_cand_ballots_index, min(int(cutoff), len(single_cand_ballots_index)))
        rand_winners2 = random.sample(cand_ballots_index, int(cutoff) - len(rand_winners1))
        rand_winners = rand_winners1 + rand_winners2

        # remove winning ballots from simulation
        for index in sorted(rand_winners, reverse=True):
            del ballot_list[index]

        # remove candidate from rest of ballots
        _remove_cand(cand, ballot_list)
