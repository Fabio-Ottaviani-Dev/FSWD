#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension # https://flask-debugtoolbar.readthedocs.io/en/latest/
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
#from flask_wtf import Form (deprecate!)
from flask_wtf import FlaskForm
from forms import *
from models import Artist, Venue, Show

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#
    # TODO: connect to a local postgresql database
    # **DONE**

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Filters
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Venues >> Create
#----------------------------------------------------------------------------#
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    #       on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # **DONE**

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        newVenue = Venue(
            name          = request.form.get('name'),
            city          = request.form.get('city'),
            state         = request.form.get('state'),
            address       = request.form.get('address'),
            phone         = request.form.get('phone'),
            facebook_link = request.form.get('facebook_link'),
            genres        = request.form.getlist('genres')
        )
        db.session.add(newVenue)
        db.session.commit()
        flash('Venue ' + newVenue.name + ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' + newVenue.name + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
        return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Venues >> Read >> Get: All
#----------------------------------------------------------------------------#
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # **DONE**

@app.route('/venues')
def venues():

    venues = db.session.query(
        func.array_agg(Venue.name).label('names'),
        func.array_agg(Venue.id).label('ids'),
        Venue.city,
        Venue.state
    ).group_by(
        Venue.city,
        Venue.state
    ).all()

    response = []
    for row in venues:
        response.append({
        'city':     row.city,
        'state':    row.state,
        'venues': [{
            'id':   venueId,
            'name': venueName,
            'num_upcoming_shows': len(Show.query.filter(Show.venue_id==venueId, Show.start_time > datetime.now()).all())
        } for venueId, venueName in zip(row.ids, row.names)]
    })
    return render_template('pages/venues.html', areas=response);

#----------------------------------------------------------------------------#
# Venues >> Read >> Search
#----------------------------------------------------------------------------#
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    # **DONE**

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search}%')).all()
    response = {
        'count':    len(venues),
        'data':     venues
    }
    return render_template('pages/search_venues.html', results=response, search_term=search)

#----------------------------------------------------------------------------#
# Venues >> Read >> Get: venue_id
#----------------------------------------------------------------------------#
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # **DONE**

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    if venue == None:
        abort(404)

    shows = Show.query.filter(Show.venue_id==venue_id).join(Artist, Show.artist_id == Artist.id).all()

    upcoming_shows = [{
        'artist_id':            show.artist.id,
        'artist_name':          show.artist.name,
        'artist_image_link':    show.artist.image_link,
        'start_time':           show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    } for show in shows if show.start_time > datetime.now()]

    past_shows = [{
        'artist_id':            show.artist.id,
        'artist_name':          show.artist.name,
        'artist_image_link':    show.artist.image_link,
        'start_time':           show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    } for show in shows if show.start_time <= datetime.now()]

    response = {
        'id':                   venue.id,
        'name':                 venue.name,
        'genres':               venue.genres,
        'city':                 venue.city,
        'state':                venue.state,
        'phone':                venue.phone,
        'website':              venue.website,
        'facebook_link':        venue.facebook_link,
        'seeking_talent':       venue.seeking_talent,
        'seeking_description':  venue.seeking_description,
        'image_link':           venue.image_link,
        'past_shows':           past_shows,
        'upcoming_shows':       upcoming_shows,
        'past_shows_count':     len(past_shows),
        'upcoming_shows_count': len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=response)

#----------------------------------------------------------------------------#
# Venues >> Update
#----------------------------------------------------------------------------#
    # TODO: populate form with values from venue with ID <venue_id>
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    # **DONE**

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(
        name            = venue.name,
        city            = venue.city,
        state           = venue.state,
        phone           = venue.phone,
        facebook_link   = venue.facebook_link,
        genres          = venue.genres,
        address         = venue.address
    )
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue               = Artist.query.get(venue_id)
        venue.name          = request.form.get('name')
        venue.city          = request.form.get('city')
        venue.state         = request.form.get('state')
        venue.phone         = request.form.get('phone')
        venue.facebook_link = request.form.get('facebook_link')
        venue.genres        = request.form.getlist('genres')
        venue.address       = request.form.get('address')
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))

#----------------------------------------------------------------------------#
# Venues >> Delete
#----------------------------------------------------------------------------#
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    # **DONE**

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    # **NOUP**

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('index'))

#----------------------------------------------------------------------------#
# Artist >> Create
#----------------------------------------------------------------------------#
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    #       on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    # **DONE **

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        newArtist = Artist(
    		name          = request.form.get('name'),
    		city          = request.form.get('city'),
    		state         = request.form.get('state'),
    		phone         = request.form.get('phone'),
    		genres        = request.form.get('genres'),
    		facebook_link = request.form.get('facebook_link'),
        )
        db.session.add(newArtist)
        db.session.commit()
        flash('Artist ' + newArtist.name + ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' + newArtist.name + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
        return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Artists >> Read >> Get: All
#----------------------------------------------------------------------------#
    # TODO: replace with real data returned from querying the database
    # **DONE**

@app.route('/artists')
def artists():
    response = Artist.query.all()
    return render_template('pages/artists.html', artists=response)

#----------------------------------------------------------------------------#
# Artists >> Read >> Search
#----------------------------------------------------------------------------#
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # **DONE**

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search}%')).all()
    response = {
        'count':    len(artists),
        'data':     artists
    }
    return render_template('pages/search_artists.html', results=response, search_term=search)

#----------------------------------------------------------------------------#
# Artists >> Read >> Get: artist_id
#----------------------------------------------------------------------------#
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # **DONE**

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    if artist == None:
        abort(404)

    shows = Show.query.filter(Show.artist_id==artist_id).join(Venue, Show.venue_id == Venue.id).all()

    upcoming_shows = [{
        'venue_id':             show.venue.id,
        'venue_name':           show.venue.name,
        'venue_image_link':     show.venue.image_link,
        'start_time':           show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    } for show in shows if show.start_time > datetime.now()]

    past_shows = [{
        'venue_id':             show.venue.id,
        'venue_name':           show.venue.name,
        'venue_image_link':     show.venue.image_link,
        'start_time':           show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    } for show in shows if show.start_time <= datetime.now()]

    response = {
        'id':                   artist.id,
        'name':                 artist.name,
        'genres':               artist.genres,
        'city':                 artist.city,
        'state':                artist.state,
        'phone':                artist.phone,
        'website':              artist.website,
        'facebook_link':        artist.facebook_link,
        'seeking_venue':        artist.seeking_venue,
        'seeking_description':  artist.seeking_description,
        'image_link':           artist.image_link,
        'past_shows':           past_shows,
        'upcoming_shows':       upcoming_shows,
        'past_shows_count':     len(past_shows),
        'upcoming_shows_count': len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=response)

#----------------------------------------------------------------------------#
# Artists >> Update
#----------------------------------------------------------------------------#
    # TODO: populate form with fields from artist with ID <artist_id>
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    # **DONE**

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(
        name            = artist.name,
        city            = artist.city,
        state           = artist.state,
        phone           = artist.phone,
        genres          = artist.genres,
        facebook_link   = artist.facebook_link
    )
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist                  = Artist.query.get(artist_id)
        artist.name             = request.form.get('name')
        artist.city             = request.form.get('city')
        artist.state            = request.form.get('state')
        artist.phone            = request.form.get('phone')
        artist.genres           = request.form.getlist('genres')
        artist.facebook_link    = request.form.get('facebook_link')
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))

#----------------------------------------------------------------------------#
# Artists >> Delete
#----------------------------------------------------------------------------#
    # EXTRA **NOUP**


#----------------------------------------------------------------------------#
#  Shows >> Create
#----------------------------------------------------------------------------#
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # **DONE **

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        newShow = Show(
            artist_id   = request.form.get('artist_id'),
            venue_id    = request.form.get('venue_id'),
            start_time  = request.form.get('start_time')
        )
        db.session.add(newShow)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
        return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

#----------------------------------------------------------------------------#
# Shows >> Read
#----------------------------------------------------------------------------#
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # **DONE **

@app.route('/shows')
def shows():

    shows = Show.query.join(
        Artist,
        Show.artist_id == Artist.id
    ).outerjoin(
        Venue,
        Show.venue_id == Venue.id
    ).all()

    response = [{
        'venue_id':             show.venue.id,
        'venue_name':           show.venue.name,
        'artist_id':            show.artist.id,
        'artist_name':          show.artist.name,
        'artist_image_link':    show.artist.image_link,
        'start_time':           show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    } for show in shows]

    return render_template('pages/shows.html', shows=response)

#----------------------------------------------------------------------------#
# Debug / Log
#----------------------------------------------------------------------------#

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

#----------------------------------------------------------------------------#
