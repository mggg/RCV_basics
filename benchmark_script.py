import timeit
import sys
import os

SETUP = 'from model_details import Cambridge_ballot_type_webapp'


def benchmark_CS():
    code_cs = 'Cambridge_ballot_type_webapp(num_simulations=5)'
    num_runs = 10
    results = timeit.timeit(
        stmt=code_cs,
        setup=SETUP,
        number=num_runs
    )
    print(f'''
    Cambridge Sampler Benchmarking Results
    ======================================
    | Number of runs    | {num_runs:13d} |
    | Time per run      | {results/num_runs:13f} |
    | Time total        | {results:13f} |
    ''')
    print(results)


if __name__ == "__main__":
    benchmark_CS()
