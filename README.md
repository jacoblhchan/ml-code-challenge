#  Data Science Code Challenge
## Note from Jacob
The pre-trained model is too large up push to github, so the currently the api does not work without a path to the trained model. Noramlly, the model is host on the cloud, which avoid this problem. To run please point to path in this [file](services/api/src/sentiment_analyzer/sentiment_analysis.py)
## Evaluation Criteria

>We are looking for clean, well organized code, comments and commits that demonstrate your ML engineering, system architecture and software design pattern skills.

### Expectations
Technologies in this test:

- PostGres
- Python
- Jupyter Notebook
- Docker/Docker-compose
- Flask (API)
- PyTorch (classifier, distilbert)
- HuggingFace NLP transformers library
- Google Colab

At  we use AI in our core product, and we expect our machine learning engineers to train, deploy, tune & scale deep learning models on microservices architecture:
1. Train a deep learning model
    - Import data
    - Split data to test/train
    - Train a PyTorch model
    - Model Accuracy
    - Model Inference 
    - Model Optimization
    - Model Quantization
2. Wrap the model in a dockerized microservice
    - Reading/Writing data to a PostGres DB
    - Creating API endpoints using Flask
    - Running a PyTorch model attached to those endpoints

> Note: This test should take you no more than 3-5 hours.
<br />
<br />

# Table of Contents
1. [Model Training / Optimization (Step 1)](#model-training-/-optimization-Step-1)
2. [API (Step 2) - Predict Movie Review Sentiment](#API-Step-2---Predict-Movie-Review-Sentiment)
    - [API Code Setup](API-code-setup)
    - [Getting started](#getting-started)
        - [Docker Compose](#docker-compose)
        - [Docker Compose Architecture](#docker-compose-architecture)
            - [Database](#database)
            - [API](#api)
                - [API Architecture](#api-architecture)
                - [API Patterns](#api-patterns)
            - [Data access](#data-access)
            - [Testing](#testing)
            - [Best practices](#best-practices)

<br />
<br />

# Model Training / Optimization (Step 1)
> In this step you will analyze, train, carry out inferrence, optimize, and quantize a PyTorch model.

1. Refer to the instructions in the Jupyter Notebook to complete the machine learning portion of the challenge:
[Model Classifier Code Challenge Notebook](/notebooks/classifier_code_challenge.ipynb).
1. If you don't have your own GPU / notebook environment you can use Google Colab to run your code (for free): [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb).
1. Use what you know about best practices in code, comments, git usage, system architecture & software design patterns to show us your best work.
1. After completing the steps in the notebook save your notebook work back to your repository
1. Download your trained model to later use in the next part of the challenge.

<br />
<br />

# API (Step 2) - Predict Movie Review Sentiment
>Using what you know about the model learned in step 1, wrap your movie review sentiment predictor in an API service.


## Story

_As a user, I want to provide a movie review sentence (input) and have the API pass back a sentiment / confidence score (output)._ 
 
## Description

The user should be able to provide a movie review about a movie, and the the API run the movie review sentiment model, then pass back a sentiment.

The API should have the following fields:
- **id** _(integer)_ 
- **sentence** _(textfield)_ The original movie review sentence from the user
- **sentiment_score** _(float)_ Returned sentiment score from the model
- **confidence** _(float)_ Returned confidence score from the model
- **created_on** _(timestamp)_ Time Stamp when the prediction was created
- **updated_on** _(timestamp)_ Time Stamp when the prediction was updated


## Required features

- [API] Add a POST route, called `create_review`, to the Sentiment blueprint for creating a new movie review sentiment
    - This should make a POST request to a new API endpoint at `/sentiments/` with the movie review sentence. If the request is successful, the review should be saved to the PostGres DB, and should be now viewable in the `/` endpoint.

## Acceptance criteria

1. The trained model from step 1 was added to the API framework
1. The API endpoint passes a movie review sentence as a parameter to the classifier model, and the model passes back a sentiment score & confidence score
1. The original sentence, score & confidence from step 2 was saved to the PostGres database
1. You can now see the new sentiment / moview review created in step 3 in the `/sentiments/` and `/sentiments/<id>` endpoints
1. You have a 90%+ code coverage for unit tests for your API code

<br />
<br />

# API Code Setup

## Getting started

The _ Data Science Code Challenge_ is built on top of Docker and Docker Compose to ease the process of setting up multiple services and connecting them.

To get started, make sure that Docker and Docker Compose are installed correctly on your system. Then:

1. Clone the repository and create your own original branch (from which you will submit a Github pull request once the task is complete)
1. Add a `.env` file to the root of the repository and add `EMAIL_ADDRESS=<YOUR_EMAIL_ADDRESS>`, where `<YOUR_EMAIL_ADDRESS>` is replaced with any email address.
1. Run `docker-compose up -d`

_NOTE: Your OS may prompt you to allow Docker to access one of your volumes. You must grant those permissions to enable the development environment._

These commands will start, configure, and connect all of the services used in _ Data Science Code Challenge_. These services include a database, database administration tool, API, and Web interface.


## Docker Compose

You'll benefit from a minimal knowledge of Docker and Docker Compose while using this repository.

- [Docker](https://docs.docker.com/develop/)
- [Docker Compose](https://docs.docker.com/compose/)

When we started the development environment we used the `-d` option. Use of the `-d` option makes Docker Compose run in the background. Without this option, the logging wouldn't be very helpful. To see the log output from any of the services, simply run `docker-compose logs -f <SERVICE_NAME>` (ex: `docker-compose logs -f api` or `docker-compose logs -f db`).

By default, Docker Compose will not rebuild a container on `docker-compose up` for performance reasons. If you feel the need to alter a service's configuration in [docker-compose.yml](docker-compose.yml) or in the service's Dockerfile, remember to rebuild the container using `docker-compose up -d --build --no-deps <SERVICE_NAME>` (ex: `docker-compose up -d --build api`).


## Docker Compose Architecture

The following section outlines the architecture of the _ Data Science Code Challenge_ application. While this section provides a good overview, it's also important to understand how each service is built by inspecting [docker-compose.yml](docker-compose.yml) and the service's Dockerfile.


## Database

_ Data Science Code Challenge_'s data persistence layer is built using Postgres. Additionally, a PG Admin service is provided to ease the burden of interacting with the database.

By default the Postgres database can be found at http://localhost:5432 and PG Admin can be accessed at http://localhost:5050. The default credentials for each of these services are defined in [docker-compose.yml](docker-compose.yml). The ports and credentials can be overridden by adding the appropriate environment variables to the [.env](.env) file that you created earlier, and in some cases by editing the [PG Admin configuration file](services/db-admin/servers.json).


## API

The API for _ Data Science Code Challenge API_ is built using Python and the popular Flask web framework.

By default, the API can be accessed at http://localhost:5051.

### API Architecture

_ Data Science Code Challenge API_ is built on the Flask and SQLAlchemy ecosystem. An understanding of those technologies is beneficial for working in this repository.


### API Patterns

The API makes use of a couple of Flask patterns for decomposition and testing.

The first is the [Blueprint Pattern](https://flask.palletsprojects.com/en/1.1.x/blueprints/). Blueprints are found under [services/api/src/blueprints](services/api/src/blueprints). Blueprints allow us to break down our code base into smaller, related chunks.

The second pattern is the [Application Factory Pattern](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/). The factory allows us to provide configuration to our application on demand and offers a cleaner bootstrapping process (see [services/api/src/__init__.py](services/api/src/__init__.py)) and greater control over configuration during unit testing.


### Data Access

_ Data Science Code Challenge API_ accesses the database using [SQLAlchemy](https://docs.sqlalchemy.org/en/13/), a popular ORM for Python, and the Flask extension [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/). Database schema migrations are managed by [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/).

Before the application starts, Flask-Migrate migrations are executed to ensure that the database schema is in sync with the models defined in the API.

You should test Flask-Migrate migrations before making commits. You can do this by running the following commands from an interactive terminal inside the API container. To start the interactive terminal, run `docker-compose exec api <COMMAND>`, where `<COMMAND>` is one of the following:

- `flask db revision -m "Create Campaign table"` to generate a new migration. You can find the new file under [services/api/migrations/versions/](services/api/migrations/versions).
- `flask db upgrade` to run all migrations up to the latest revision
- `flask db downgrade` to undo the last revision

 
 ### Testing

_ Data Science Code Challenge API_ uses [PyTest](https://docs.pytest.org/en/latest/) and [PyTest-watch](https://github.com/joeyespo/pytest-watch) for automated testing. The test suite is run immediately before the API is initialized. If the tests are not passing, the API server will not start.

To automatically run the test suite when a file changes, start PyTest-watch with the following commands:

1. `docker-compose exec api sh`
1. `ptw`
 
 
 ### Best practices
 
 Pay special attention to the following best practices:
 
 - **_Test_** All routes should be feature tested (actually accessing a database). Feel free to manipulate the database to achieve the state you need. _See the files under [test/](services/api/test/blueprints) for examples._
 - **_Understand your queries_** SQLAlchemy: understand what raw queries are actually executed when using SQLAlchemy models.


