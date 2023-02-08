#!/bin/sh

# Run test suite. Running these here is strictly for development convenience. This would
#  be a bad idea in production, given the time it takes to start the API.
pytest

# Upgrades the database with the latest migrations. This should not be done here. It's
#  considered best practice to separate these operations. This is merely for convenience.
flask db upgrade

# Start the Flask development server. The Flask CLI runs a non-performance and potentially unstable
#  version of Flask that is unsuitable for production environments. This is merely for convenience.
flask run --host=0.0.0.0 --port=${PORT}