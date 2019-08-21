import json
import dateutil.parser
import babel
from flask import (
    Flask,
    abort,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
from models import Venue, Show, Artist

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
# import models
migrate = Migrate(app, db)


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
def index():
    """
        render main page
    """
    return render_template('pages/home.html')


@app.route('/venues')
def venues():
    """
            show venues arranged by
    """
    data = [venue.list
            for venue in Venue.query.distinct(Venue.city, Venue.state).all()]

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search = request.form.get('search_term', None)
    venues = Venue.query.filter(
        Venue.name.ilike("%{}%".format(search)))
    data = list(
        map(lambda venue: venue.short_format, venues.all())
    )
    response = {
        "count": venues.count(),
        "data": data
    }
    return render_template('pages/search_venues.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """
            shows the venue page with the given venue_id
    """
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
    except NoResultFound:
        abort(404)
    data = venue.format_with_shows
    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    try:
        venue = Venue(
            name=form.name.data,
            genres=json.dumps(form.genres.data),  # array json
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
        )
        venue.insert()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
        venue.delete()
        flash("venue has delete")
    except NoResultFound:
        abort(404)


@app.route('/artists')
def artists():
    data = list(
        map(lambda artist: artist.short_format, Artist.query.all())
    )
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term', None)
    artists = Artist.query.filter(
        Artist.name.ilike("%{}%".format(search)))
    data = list(
        map(lambda artist: artist.short_format, artists.all())
    )
    response = {
        "count": artists.count(),
        "data": data
    }
    return render_template('pages/search_artists.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        artist = Artist.query.filter_by(id=artist_id).one()
    except NoResultFound:
        abort(404)
    data = artist.format_with_shows
    return render_template('pages/show_artist.html',
                           artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist_object = Artist.query.filter_by(id=artist_id).one()
    artist = artist_object.long_format
    form = ArtistForm(data=artist)
    return render_template('forms/edit_artist.html',
                           form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    try:
        artist = Artist.query.filter_by(id=artist_id).one()
        artist.name = form.name.data,
        artist.genres = json.dumps(form.genres.data),  # array json
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.facebook_link = form.facebook_link.data,
        artist.image_link = form.image_link.data,
        artist.update()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue_object = Venue.query.filter_by(id=venue_id).one()
    venue = venue_object.long_format
    form = VenueForm(data=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    form = VenueForm(request.form)
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
        venue.name = form.name.data,
        venue.address = form.address.data,
        venue.genres = json.dumps(form.genres.data),  # array json
        venue.city = form.city.data,
        venue.state = form.state.data,
        venue.phone = form.phone.data,
        venue.facebook_link = form.facebook_link.data,
        venue.image_link = form.image_link.data,
        venue.update()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')

    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    try:
        artist = Artist(
            name=form.name.data,
            genres=json.dumps(form.genres.data),  # array json
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
        )
        artist.insert()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = list(
        map(lambda show: show.long_format, Show.query.all())
    )
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)
    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        show.insert()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        flash('An error occurred. Show could not be listed.')

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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
            )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run()
