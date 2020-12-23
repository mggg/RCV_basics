import timeit

SETUP = '''
  from model_details import Cambridge_ballot_type_webapp
'''


def benchmark_CS():
    code_cs = '''
    Cambridge_ballot_type_webapp()
  '''
    num_runs = 10
    results = timeit.timeit(
        setup=SETUP,
        stmt=code_cs,
        number=num_runs
    )
    print(results)


if __name__ == "__main__":
    benchmark_CS()
