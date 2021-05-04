# Simulating Racially Polarized Ranked Choice Voting

Copy and adapt `run_all_models_and_print_output.py` to cycle through all four models and all five scenarios. The results will be printed as rows of values separated by &s for easy input into LaTeX tables. 

In the `docs` directory, the `template_table.tex` file contains a basic template for recording these results, including a very brief overview of the models and a blank table with headers.

## Getting started

The application was built using Python 3.7.5, and all dependent packages can be installed from the `requirements.txt` file by running the following:

```bash
pip install -r requirements.txt
```

## Running the RCV API Server

To run the Ranked Choice Vote API server, one need only run the `app.py` script:

```bash
python app.py
```

## Deploying the RCV API Server

As of 11/2020, the API server is deployed on Heroku. New versions of the server are automating deployed when code is pushed to the `heroku_prod` branch.

For a quick walkthrough on how the API Server is deployed through Heroku, review this article: https://stackabuse.com/deploying-a-flask-application-to-heroku/

For first-time users of Heroku who need to set up accounts and install the Heroku CLI, review this guide: https://devcenter.heroku.com/articles/getting-started-with-python#set-up

N.B. that heroku's auto-deploy will ignore the port used in the local flask app. This needs to be taken into account when connecting to the API via external web applications.


## Benchmarking

To understand how runtimes vary across each RCV model, modify the  `benchmark_script.py` file to ensure that `main` calls the `benchmark` function once for each model_type.

For a given model type, one can get line-level runtime performance by using the `line_profiler` package installed. For detailed documentation, see [here](https://github.com/pyutils/line_profiler). In general you should do the following:

1. For the model type you want to benchmark, decorate each function you want profiled with the `@profile` decorator in the corresponding `models/model_type_of_choice.py` file.

2. Modify `benchmark_script.py` to only call `benchmark` for the model type of interest.

3. From the project directory, run `kernprof -l -v benchmark_script.py`. This will generate a `benchmark_script.py.lprof` file that contains line-level profiling for the functions decorated with `@profile`. Additionally, the `-v` means you will automatically view that file after execution.

4. To store this file for posterity, rename it sensible and move it to `docs/benchmarking`.

5. To view a `*.lprof` file again, run `python -m line_profiler path/to/*.lprof`.

6. NOTE: when done profiling, remove the `@profile` decorators; they will leave the code in an invalid state outside of benchmarking.


