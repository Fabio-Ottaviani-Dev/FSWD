import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://Billy@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 1. createdb fyyur && psql fyyur
# 2. python3 models.py db init
