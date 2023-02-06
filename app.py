#----------------------------------------------------------------------------#
# Notes
#----------------------------------------------------------------------------#
# I had to modernize the code to work with the latest version of Python, Flask, and SQLAlchemy. 
# I decided to put the models in a separate file, models.py, and import them into app.py.
#
# Steps to run the application:
# 1. Create a db: `createdb fyyur`; The postgres password must be `abc`;
# 2. Start the server: `python app.py`;
# 3. Init the DB: `flask db upgrade`;
# 4. Seed the DB: `python seed.py`;
# 5. Open the browser: `http://127.0.0.1:3000`.
#
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from sqlalchemy import func, exists, or_
from pprint import pprint

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

from app_instance import app, db, migrate

with app.app_context():
  #----------------------------------------------------------------------------#
  # Models.
  #----------------------------------------------------------------------------#

  from models import *

  #----------------------------------------------------------------------------#
  # Forms.
  #----------------------------------------------------------------------------#

  from forms import *

  #----------------------------------------------------------------------------#
  # Filters.
  #----------------------------------------------------------------------------#

  def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

  app.jinja_env.filters['datetime'] = format_datetime

  #----------------------------------------------------------------------------#
  # Controllers.
  #----------------------------------------------------------------------------#

  @app.route('/')
  def index():
    return render_template('pages/home.html')

  #  Venues
  #  ----------------------------------------------------------------

  @app.route('/venues/search', methods=['POST'])
  @app.route('/venues')
  def venues():
    is_search = request.method == 'POST'
    search_term = request.form.get('search_term', '')
    results_count = 0

    if is_search:
      query = City.query.filter(exists().where(Venue.city_id == City.id).where(Venue.name.ilike(f'%{search_term}%')))
    else:
      query = City.query.filter(exists().where(Venue.city_id == City.id))

    cities = query.order_by('id').all()

    for city in cities:
      for venue in city.venues:
        if not is_search or (is_search and search_term.lower() in venue.name.lower()):
          results_count += 1

    return render_template('pages/venues.html', cities=cities, search_term=search_term, results_count=results_count)

  @app.route('/venues/<int:venue_id>')
  def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=venue)

  #  Create Venue
  #  ----------------------------------------------------------------

  @app.route('/venues/create', methods=['GET'])
  def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

  @app.route('/venues/create', methods=['POST'])
  def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

  @app.route('/venues/<venue_id>', methods=['DELETE'])
  def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

  #  Artists
  #  ----------------------------------------------------------------
  @app.route('/artists/search', methods=['POST'])
  @app.route('/artists')
  def artists():
    is_search = request.method == 'POST'
    search_term = request.form.get('search_term', '')
    results_count = 0

    if is_search:
      artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).order_by(Artist.name).all()
      results_count = len(artists)
    else:
      artists = Artist.query.order_by(Artist.name).all()

    return render_template('pages/artists.html', artists=artists, search_term=search_term, results_count=results_count)

  @app.route('/artists/<int:artist_id>')
  def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    data1={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "past_shows": [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "start_time": "2019-05-21T21:30:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data2={
      "id": 5,
      "name": "Matt Quevedo",
      "genres": ["Jazz"],
      "city": "New York",
      "state": "NY",
      "phone": "300-400-5000",
      "facebook_link": "https://www.facebook.com/mattquevedo923251523",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "past_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data3={
      "id": 6,
      "name": "The Wild Sax Band",
      "genres": ["Jazz", "Classical"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "432-325-5432",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "past_shows": [],
      "upcoming_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
      }],
      "past_shows_count": 0,
      "upcoming_shows_count": 3,
    }
    data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data)

  #  Update
  #  ----------------------------------------------------------------
  @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
  def edit_artist(artist_id):
    form = ArtistForm()
    artist={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

  @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
  def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))

  @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
  def edit_venue(venue_id):
    form = VenueForm()
    venue={
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

  @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
  def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

  #  Create Artist
  #  ----------------------------------------------------------------

  @app.route('/artists/create', methods=['GET'])
  def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

  @app.route('/artists/create', methods=['POST'])
  def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


  #  Shows
  #  ----------------------------------------------------------------

  @app.route('/shows')
  def shows():
    # displays list of shows at /shows
    shows = Show.query.filter(Show.start_time >= datetime.now()).order_by(Show.start_time.desc()).all()
    return render_template('pages/shows.html', shows=shows)

  @app.route('/shows/create')
  def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

  @app.route('/shows/create', methods=['POST'])
  def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

  @app.errorhandler(404)
  def not_found_error(error):
      return render_template('errors/404.html'), 404

  @app.errorhandler(500)
  def server_error(error):
      return render_template('errors/500.html'), 500


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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
