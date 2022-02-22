# Message In a Bottle - API Gateway


[![CircleCI](https://circleci.com/gh/NennoMP/mib-api-gateway.svg?style=svg)](https://app.circleci.com/pipelines/github/NennoMP/mib-api-gateway)
[![codecov](https://codecov.io/gh/NennoMP/mib-api-gateway/branch/main/graph/badge.svg?token=APB8A4ZRIF)](https://codecov.io/gh/NennoMP/mib-api-gateway)

This is the source code of My Message in a Bottle API-gateway microservice, project of **Advanced Software Engineering** course of the MSc in Computer Science,
University of Pisa.

#### Members

Mark with *bold* the person(s) that has developed this microservice.

|Name and Surname    | Email                         |
|--------------------|-------------------------------|
|*Laura Norato*      |l.norato@studenti.unipi.it     |
|*Emanuele Albertosi*|20783727@studenti.unipi.it     |
|*Michele Zoncheddu* |m.zoncheddu@studenti.unipi.it  |
|*Alessio Russo*     |a.russo65@studenti.unipi.it    |
|*Matteo Pinna*      |m.pinna10@studenti.unipi.it    |


## Overview
This microservice implements the API-gateway logic.

## Instructions
The available environments are:

- debug
- development
- testing
- production

If you want to run the appliction with development environment, or you are developing the application and you want to have the debug tools, you can start the application locally (without `docker-compose`) by executing `bash run.sh`.

**Note:** if you use `docker-compose up` you are going to startup a production ready microservice, hence postgres will be used as default database and gunicorn will serve your application.

You can run the entire application by following the instructions on the main repository mib-main. However, if you would like to separately run this microservice take a look at the steps below.

### Initialization
First, you need to setup create a virtual environment and to install all requirements. Run these commands inside **mib-api-gateway** root:

1. Create a virtual environment with `virtualenv venv`.
3. Activate it with `source venv/bin/activate` or `source venv/scripts/activate`.
4. Install all requirements needed with `pip install -r requirements.dev.txt`.

**WARNING**: the static contents are inside the directory nginx/static,
so if you want to run application without nginx you have to copy
the static directory inside mib folder.

### Python dotenv
Each time you start a new terminal session, you have to
set up all the environment variables that projects requires.
When the variables number increases, the procedures needed to run
the project becomes uncomfortable. 

To solve this problem we have introduced the python-dotenv dependency,
but only for development purposes.
You can create a file called `.env` that will be interpreted each time
that you run the python project.
Inside `.env` file you can store all variables that project requires.
The `.env` file **MUST NOT** be added to repository and must kept
local. You can find an example with `.env-example` file.

### Dependencies splitting

Each environment requires its dependency. For example
`production` env does not require the testing frameworks.
Also to keep the docker image clean and thin we have
to split the requirements in 2 files.

- `requirements.txt` is the base file.
- `requirements.dev.txt` extends base file and it contains all development requirements,
for example pytest.
- `requirements.prod.txt` extends base file and it contains the production requirements,
for example gunicorn and psycopg2.

**IMPORTANT:** the Docker image uses the only the production requirements.

### Nginx and Gunicorn

Nginx will serve static contents directly and will use gunicorn
to serve app pages from flask wsgi.
You can start gunicorn locally with the command

`gunicorn --config gunicorn.conf.py wsgi:app`

**WARNING** gunicorn it's not able to read
the .env files, so you have to export the variable, for
example by issuing the command `source .env`.


### Docker compose

To run services with `docker-compose up`, first you
have to configure the environment variables
inside the env_file, and specify it with the parameter `--env-file`.
An example of env_file is added to repository and it's called
env_file_example.

**WARNING:** please do not track your env_file!

The complete command to run this service with docker is the following:

`docker-compose --env-file <your-env-file> up`

### Nginx orchestrator

We have created a specific documentation file for [nginx-orchestrator](./nginx-orchestrator/README.md)

### Run
You can now run the microservice running the following commands:

1. Run the microservice with `bash run.sh` (environment is automatically set to development).

### Testing
In order to execute the tests you need, if you haven't already, to install the requirements by following the steps mentioned above. When you're done, you can run the tests:

1. Set Flask environment to testing with `export FLASK_ENV=testing`
2. Run the tests with `pytest`

The tests are set to file when the coverage is below 90%.

You can also specify one or more specific test files, in order to run only those specific tests. In case you also want to see the overall coverage of the tests, execute the following command:

`python -m pytest --cov=mib`

In order to know what are the lines of codes which are not covered by the tests, execute the command:

`python -m pytest --cov-report term-missing`