#----------------------------------------------------------------------------#
# Docs:
# https://flask-migrate.readthedocs.io/en/latest/#using-flask-script
# python3 models.py db init, migrate, upgrade, downgrade.
#----------------------------------------------------------------------------#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# TODO:
# 1. Implement any missing fields, as a database migration using Flask-Migrate
# 2. Implement Show and Artist models, and complete all model relationships and
#    properties, as a database migration.
# ** DONE **
#----------------------------------------------------------------------------#

class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(2), nullable=False)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(150))
    facebook_link = db.Column(db.String(150))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(255))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(150))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('artist', lazy=True))

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime())

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    manager.run()
