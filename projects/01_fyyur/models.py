
#----------------------------------------------------------------------------#
# Docs:
# https://flask-migrate.readthedocs.io/en/latest/#using-flask-script
# python3 models.py db init, migrate, upgrade, downgrade.

# How to print instances of a class using print()
# https://stackoverflow.com/questions/1535327/how-to-print-instances-of-a-class-using-print
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
# Models
#----------------------------------------------------------------------------#
# TODO:
# 1. Implement any missing fields, as a database migration using Flask-Migrate
# 2. Implement Show and Artist models, and complete all model relationships and
#    properties, as a database migration.
# ** DONE **
#----------------------------------------------------------------------------#
'''
class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(2), nullable=False)
'''

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    # state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(150))
    website = db.Column(db.String(150))
    genres = db.Column(db.ARRAY(db.String))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(255))
    shows = db.relationship('Show', backref=db.backref('venue', lazy=True))

    def __repr__(self):
        return f'<Venue: ID: {self.id}, Name: {self.name},  City: {self.city}>'

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    # state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(150))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('artist', lazy=True))

    def __repr__(self):
        return f'<Artist: ID: {self.id}, Name: {self.name},  City: {self.city}>'

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime())

    def __repr__(self):
        return f'<Show: ID: {self.id}, artist_id: {self.artist_id},  venue_id: {self.venue_id}>'

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    manager.run()
