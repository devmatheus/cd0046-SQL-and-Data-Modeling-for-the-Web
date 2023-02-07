#----------------------------------------------------------------------------#
# Notes
#----------------------------------------------------------------------------#
# I had to modernize the code to work with the latest version of Python, Flask, and SQLAlchemy. 
# I decided to put the models in a separate file, models.py, and import them into app.py.
# 
# Screen recording: https://d.pr/v/RaPBhQ
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

import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from sqlalchemy import exists

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

  try:
    from forms import *
  except:
    print('Error: Database not migrated. Please run `flask db upgrade && python seed.py`.')

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

  @app.route('/api/cities', methods=['GET'])
  def api_cities():
    state_code = request.args.get('state_code')
    if state_code:
      cities = City.query.filter_by(state_code=state_code).order_by(City.name).all()
    else: 
      cities = City.query.order_by(City.name).all()

    return jsonify({city.id: city.name for city in cities})

  @app.route('/api/venues/<venue_id>', methods=['DELETE'])
  def delete_venue(venue_id):
    body = {}
    try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully deleted!')
      body['success'] = True
    except:
        db.session.rollback()
        flash('An error occurred. Venue #' + venue_id + ' could not be deleted.', 'error')
        body['success'] = False

    return jsonify(body)

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
    form = VenueForm(request.form)

    if not form.validate():
      return render_template('forms/new_venue.html', form=form)
      
    try:
      venue = Venue(
        name=request.form['name'],
        city=City.query.get(request.form['city']),
        address=request.form['address'],
        phone=request.form['phone'],
        genres=Genre.query.filter(Genre.id.in_(request.form.getlist('genres'))).all(),
        facebook_link=request.form['facebook_link'],
        image_link=request.form['image_link'],
        website=request.form['website_link'],
        seeking_talent=request.form['seeking_talent'] == 'y',
        seeking_description=request.form['seeking_description'],
      )

      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')

    return render_template('pages/home.html')

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
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist)

  #  Update
  #  ----------------------------------------------------------------
  @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
  def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

  @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
  def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)

    if not form.validate():
      return render_template('forms/edit_artist.html', form=form)

    try:
      artist = Artist.query.get(artist_id)
      artist.name = request.form['name']
      artist.city = City.query.get(request.form['city'])
      artist.phone = request.form['phone']
      artist.genres = Genre.query.filter(Genre.id.in_(request.form.getlist('genres'))).all()
      artist.facebook_link = request.form['facebook_link']
      artist.image_link = request.form['image_link']
      artist.website = request.form['website_link']
      artist.seeking_venue = request.form['seeking_venue'] == 'y'
      artist.seeking_description = request.form['seeking_description']

      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully updated!')
    except:
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.', 'error')

    return redirect(url_for('show_artist', artist_id=artist_id))

  @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
  def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

  @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
  def edit_venue_submission(venue_id):
    form = VenueForm(request.form)

    if not form.validate():
      return render_template('forms/edit_venue.html', form=form)

    try:
      venue = Venue.query.get(venue_id)
      venue.name = request.form['name']
      venue.city = City.query.get(request.form['city'])
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      venue.genres = Genre.query.filter(Genre.id.in_(request.form.getlist('genres'))).all()
      venue.facebook_link = request.form['facebook_link']
      venue.image_link = request.form['image_link']
      venue.website = request.form['website_link']
      venue.seeking_talent = request.form['seeking_talent'] == 'y'
      venue.seeking_description = request.form['seeking_description']

      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully updated!')
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.', 'error')
      
    return redirect(url_for('show_venue', venue_id=venue_id))

  #  Create Artist
  #  ----------------------------------------------------------------

  @app.route('/artists/create', methods=['GET'])
  def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

  @app.route('/artists/create', methods=['POST'])
  def create_artist_submission():
    form = ArtistForm(request.form)

    if not form.validate():
      return render_template('forms/new_artist.html', form=form)

    try:
      artist = Artist(
        name=request.form['name'],
        city=City.query.get(request.form['city']),
        phone=request.form['phone'],
        genres=Genre.query.filter(Genre.id.in_(request.form.getlist('genres'))).all(),
        facebook_link=request.form['facebook_link'],
        image_link=request.form['image_link'],
        website=request.form['website_link'],
        seeking_venue=request.form['seeking_venue'] == 'y',
        seeking_description=request.form['seeking_description'],
      )

      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', 'error')

    return render_template('pages/home.html')

  #  Shows
  #  ----------------------------------------------------------------

  @app.route('/shows')
  def shows():
    shows = Show.query.filter(Show.start_time >= datetime.now()).order_by(Show.start_time.desc()).all()
    return render_template('pages/shows.html', shows=shows)

  @app.route('/shows/create')
  def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

  @app.route('/shows/create', methods=['POST'])
  def create_show_submission():
    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )

        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.', 'error')

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
