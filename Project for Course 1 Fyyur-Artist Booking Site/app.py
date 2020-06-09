#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
Flask,
render_template,
request,
flash,
redirect,
url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from models import *
from config import DatabaseURI
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseURI.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
 


# connect to a local postgresql database
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
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

# statements are used to execute joined queries
# https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join
def adding_past_upcoming_shows(data, type, data_id):
  if type=='venue':
    past_shows=db.session.query(Show).join(Venue).filter(Show.venue_id==data_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows=db.session.query(Show).join(Venue).filter(Show.venue_id==data_id).filter(Show.start_time>datetime.now()).all()
  if type=='artist':
    past_shows=db.session.query(Show).join(Artist).filter(Show.artist_id==data_id).filter(Show.start_time<datetime.now()).all()
    upcoming_shows=db.session.query(Show).join(Artist).filter(Show.artist_id==data_id).filter(Show.start_time>datetime.now()).all()

  data.num_past_show=len(past_shows)
  data.num_upcoming_show=len(upcoming_shows)
  data.past_shows=[]
  data.upcoming_shows=[]
  for past_show in past_shows:
    data.past_shows.append({
          "artist_id": past_show.artist_id,
          "artist_name": past_show.artist.name,
          "artist_image_link": past_show.artist.image_link,
          "start_time": past_show.start_time.strftime("%m/%d/%Y, %H:%M"),
          "venue_id": past_show.venue_id,
          "venue_name": past_show.venue.name,
          "venue_image_link": past_show.venue.image_link
        })
  for upcoming_show in upcoming_shows:
    data.upcoming_shows.append({
          "artist_id": upcoming_show.artist_id,
          "artist_name": upcoming_show.artist.name,
          "artist_image_link": upcoming_show.artist.image_link,
          "start_time": upcoming_show.start_time.strftime("%m/%d/%Y, %H:%M"),
          "venue_id": upcoming_show.venue_id,
          "venue_name": upcoming_show.venue.name,
          "venue_image_link": upcoming_show.venue.image_link
        })



#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  areas=Venue.query.distinct('state', 'city').order_by('state', 'city').all()
  for area in areas:
    area.venues = Venue.query.filter_by(state=area.state, city=area.city)
  return render_template('pages/venues.html', areas=areas);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  item_to_search=request.form.get('search_term', '')
  item_to_search = '%'+item_to_search+'%'
  search_results=Venue.query.filter(Venue.name.ilike(item_to_search)).all()
  count=len(search_results)
  data=[result for result in search_results]
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  
  data=Venue.query.get_or_404(venue_id)
  # data.genres=data.genres_split()
  if db.session.query(Show).all():
    adding_past_upcoming_shows(data, 'venue', venue_id)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  # form = VenueForm(request.form)
  form = VenueForm()
  if form.validate_on_submit():
    error=False
    try:
      venue = Venue(
                  name=request.form['name'],
                  city=request.form['city'],
                  state=request.form['state'],
                  address=request.form['address'],
                  phone=request.form['phone'],
                  genres=request.form.getlist('genres'),
                  facebook_link=request.form['facebook_link'],
                  image_link=request.form['image_link'],
                  website=request.form['website'],
                  seeking_talent_ad=request.form['seeking_talent_ad'],
                  seeking_talent=True if 'seeking_talent'in request.form else False
    )
      db.session.add(venue)
    except expression:
      error=True
      print(sys.exc_info())
    finally:
      if not error:
        db.session.commit()
          # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
      
  # on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      else:
        flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
        db.session.rollback()
  else:
    flash('Venue ' + request.form['name'] + ' failed due to validation error!')
    flash(form.errors)
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    return redirect(url_for('venues'))

  except SQLAlchemyError as e:
    print(e)
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  data=Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  item_to_search=request.form.get('search_term', '')
  item_to_search = '%'+item_to_search+'%'
  search_results=Artist.query.filter(Artist.name.ilike(item_to_search)).all()
  count=len(search_results)
  data=[result for result in search_results]

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # replace with real venue data from the venues table, using venue_id
  data=Artist.query.get_or_404(artist_id)
  if db.session.query(Show).all():
    adding_past_upcoming_shows(data, 'artist', artist_id)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get_or_404(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  try:
    data=Artist.query.get_or_404(artist_id)
    data.name=request.form['name']
    data.city = request.form['city']
    data.state = request.form['state']
    data.phone = request.form['phone']
    data.facebook_link = request.form['facebook_link']
    data.genres = request.form.getlist('genres') or []
    data.image_link = request.form['image_link']
    data.website=request.form['website']
    data.seeking_venue_ad = request.form['seeking_venue_ad']
    data.seeking_venue = True if 'seeking_venue'in request.form else False

  except expression:
    error=True
  
  finally:
    if not error:
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        db.session.rollback()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # populate form with values from venue with ID <venue_id>
  venue=Artist.query.get_or_404(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error=False
  try:
    data=Venue.query.get_or_404(venue_id)
    data.name=request.form['name']
    data.city = request.form['city']
    data.state = request.form['state']
    data.phone = request.form['phone']
    data.facebook_link = request.form['facebook_link']
    data.genres = request.form.getlist('genres') or []
    data.image_link = request.form['image_link']
    data.website=request.form['website']
    data.seeking_talent_ad = request.form['seeking_talent_ad']
    data.seeking_talent = True if 'seeking_talent'in request.form else False
  except expression:
    error=True
  finally:
    if not error:
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      db.session.rollback()
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
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  form = ArtistForm()
  if form.validate_on_submit():
    error=False
    try:
      artist = Artist(
                    name=request.form['name'],
                    city=request.form['city'],
                    state=request.form['state'],
                    phone=request.form['phone'],
                    genres=request.form.getlist('genres') or [],
                    facebook_link=request.form['facebook_link'],
                    image_link=request.form['image_link'],
                    website=request.form['website'],
                    seeking_venue_ad=request.form['seeking_venue_ad'],
                    seeking_venue=True if 'seeking_venue'in request.form else False
      )
    
      db.session.add(artist)

    except expression:
        error=True
      
    finally:
      if not error:
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
      else:
        flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
        db.session.rollback()
  else:
    flash('Artist ' + request.form['name'] + ' failed due to validation error!')
    flash(form.errors)
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  data=Show.query.order_by(Show.start_time).all()
  for show in data:
    venue = Venue.query.get_or_404(show.venue_id)
    show.venue_name= venue.name
    artist = Artist.query.get_or_404(show.artist_id)
    show.artist_name= artist.name
    show.artist_image_link= artist.image_link
    show.start_time=show.start_time.strftime("%m/%d/%Y, %H:%M")
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  form = ShowForm()
  if form.validate_on_submit():
    error=False
    try:
      show = Show(
                    artist_id=request.form['artist_id'],
                    venue_id=request.form['venue_id'],
                    start_time=request.form['start_time']
      )       
      db.session.add(show)
    except expression:
      error=True
    finally:
      if not error:
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
      else:
        #on unsuccessful db insert, flash an error instead
        flash('An error occurred. Show could not be listed.')
        db.session.rollback()
  else:
    flash('Show creation failed due to validation error!')
    flash(form.errors)
  return render_template('pages/home.html')

# bad_request - 400, unauthorized - 401, forbidden - 403, not_found - 404, server_error - 500, not_processable - 422, invalid_method - 405, duplicate_resource - 409

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(400)
def server_error(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(403)
def server_error(error):
    return render_template('errors/403.html'), 403


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
