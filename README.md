# A code base for running the four main models of racially polarized ranked choice voting

Copy and adapt run_all_models_and_print_output.py to cycle through all four models and all five scenarios. The results will be printed as rows of values separated by &s for easy input into LaTeX tables.

The template_table.tex file contains a basic template for recording these results, including a very brief overview of the models and a blank table with headers.

## Getting started

The application was built using Python 3.7.5, and all dependent packages can be installed from the `requirements.txt` file by running the following:

```
pip install -r requirements.txt
```

## Running the RCV API Server

To run the Ranked Choice Vote API server, one need only run the `app.py` script:

```
python app.py
```

## Deploying the RCV API Server

As of 11/2020, the API server is deployed on Heroku. New versions of the server are automating deployed when code is pushed to the `heroku_prod` branch.

For more information on how the API Server is deployed through heroku, review this article: https://stackabuse.com/deploying-a-flask-application-to-heroku/
