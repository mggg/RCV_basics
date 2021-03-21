import timeit
import sys
import os

SETUP = '''
from models import Cambridge_ballot_type_webapp, Alternating_crossover_webapp, plackett_luce_dirichlet, bradley_terry_dirichlet
'''


def model_code(model_type):
    code = ''
    if model_type == 'CS':
        code = '''Cambridge_ballot_type_webapp(poc_share=0.42000000000000004,
        poc_support_for_poc_candidates=0.96,
        poc_support_for_white_candidates=0.040000000000000036,
        white_support_for_white_candidates=0.67,
        white_support_for_poc_candidates=0.32999999999999996,
        num_ballots=1000,
        seats_open=4,
        num_white_candidates=4,
        num_poc_candidates=4,
        voting_preferences=[1, 1, 1, 1],
        num_simulations=10)'''
    elif model_type == 'AC':
        code = '''Alternating_crossover_webapp(poc_share=0.42000000000000004,
        poc_support_for_poc_candidates=0.96,
        poc_support_for_white_candidates=0.040000000000000036,
        white_support_for_white_candidates=0.67,
        white_support_for_poc_candidates=0.32999999999999996,
        num_ballots=1000,
        seats_open=4,
        num_white_candidates=4,
        num_poc_candidates=4,
        voting_preferences=[1, 1, 1, 1],
        num_simulations=10)'''
    elif model_type == 'PL':
        code = '''plackett_luce_dirichlet(poc_share=0.42000000000000004,
            poc_support_for_poc_candidates=0.96,
            poc_support_for_white_candidates=0.040000000000000036,
            white_support_for_white_candidates=0.67,
            white_support_for_poc_candidates=0.32999999999999996,
            num_ballots=1000,
            seats_open=4,
            num_white_candidates=4,
            num_poc_candidates=4,
            concentrations=[0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476],
            num_simulations=11)'''
    elif model_type == 'BT':
        code = '''bradley_terry_dirichlet(poc_share=0.42000000000000004,
            poc_support_for_poc_candidates=0.96,
            poc_support_for_white_candidates=0.040000000000000036,
            white_support_for_white_candidates=0.67,
            white_support_for_poc_candidates=0.32999999999999996,
            num_ballots=1000,
            seats_open=4,
            num_white_candidates=4,
            num_poc_candidates=4,
            concentrations=[0.7071067811865476, 0.7071067811865476, 0.7071067811865476, 0.7071067811865476],
            num_simulations=11,)'''
    else:
        raise Exception("unknown model type: " + model_type)
    return code


def benchmark(model_type, num_runs=10):
    code = model_code(model_type)
    results = timeit.timeit(
        stmt=code,
        setup=SETUP,
        number=num_runs
    )
    print(f'''
## {model_type} model_type Benchmarking Results

| Time total    | Number of runs | Time per run  |
| :------------ | :------------- | :------------ |
| {results:13f} | {num_runs:14d} | {results/num_runs:13f} |
    ''')
    print(results)


if __name__ == "__main__":
    benchmark('BT', 5)
    # benchmark('PL', 5)
    # benchmark('CS')
    # benchmark('AC')
