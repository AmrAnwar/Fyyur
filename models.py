import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def get_genres(self):
        return json.loads(self.genres)

    @property
    def long_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.get_genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link
        }

    @property
    def format_with_shows(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.get_genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            "past_shows": list(map(lambda show: show.long_format_artist,
                                   self.past_shows.all())),
            "upcoming_shows": list(map(lambda show: show.long_format_artist,
                                       self.upcoming_shows.all())),
            "past_shows_count": self.past_shows.count(),
            "upcoming_shows_count": self.upcoming_shows.count(),
        }

    @property
    def short_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': self.past_shows.count()  # TODO,
        }

    @property
    def list(self):
        return{
            "city": self.city,
            "state": self.state,
            "venues": list(
                map(lambda venue: venue.short_format,
                    Venue.query.filter_by(city=self.city,
                                          state=self.state).all())
            ),

        }

    @property
    def past_shows(self):
        return Show.query.filter(Show.start_time < datetime.datetime.now(),
                                 Show.venue_id == self.id)

    @property
    def upcoming_shows(self):
        return Show.query.filter(Show.start_time > datetime.datetime.now(),
                                 Show.venue_id == self.id)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))

    @property
    def get_genres(self):
        return json.loads(self.genres)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def long_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.get_genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link
        }

    @property
    def short_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': self.past_shows.count()
        }

    @property
    def past_shows(self):
        return Show.query.filter(Show.start_time < datetime.datetime.now(),
                                 Show.artist_id == self.id)

    @property
    def upcoming_shows(self):
        return Show.query.filter(Show.start_time > datetime.datetime.now(),
                                 Show.artist_id == self.id)

    @property
    def format_with_shows(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.get_genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            "past_shows": list(map(lambda show: show.long_format_venue,
                                   self.past_shows.all())),
            "upcoming_shows": list(map(lambda show: show.long_format_venue,
                                       self.upcoming_shows.all())),
            "past_shows_count": self.past_shows.count(),
            "upcoming_shows_count": self.upcoming_shows.count(),
        }


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('Artist.id'), nullable=False
    )
    artist = db.relationship(
        'Artist',
        backref=db.backref('shows', cascade="all,delete")
    )
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey('Venue.id'), nullable=False
    )
    venue = db.relationship(
        'Venue',
        backref=db.backref('shows', cascade="all,delete")
    )  # delete all the shows if cascade

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def long_format(self):
        """
        long_format works with the venue and artist page
        """
        return{
            "venue_id": self.venue.id,
            "venue_name": self.venue.name,
            "artist_id": self.artist.id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "venue_image_link": self.venue.image_link,
            "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        }

    @property
    def long_format_venue(self):
        """
        long_format works with the venue and artist page
        """
        return{
            "venue_id": self.venue.id,
            "venue_name": self.venue.name,
            "venue_image_link": self.venue.image_link,
            "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        }

    @property
    def long_format_artist(self):
        """
        long_format works with the venue and artist page
        """
        return{
            "artist_id": self.artist.id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        }
