import datetime
from app_instance import db

class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    cities = db.relationship('City', backref='state', lazy=True)

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state_code = db.Column(db.String(2), db.ForeignKey('states.code'), nullable=False)
    venues = db.relationship('Venue', backref='city', lazy=True)
    artists = db.relationship('Artist', backref='city', lazy=True)

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

venue_genres = db.Table('venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.relationship('Genre', secondary=venue_genres, lazy='subquery',
        backref=db.backref('venues', lazy=True))

    @property
    def upcoming_shows(self):
        return Show.query.filter(Show.venue_id == self.id).filter(Show.start_time >= datetime.datetime.now()).all()
    
    @property
    def past_shows(self):
        return Show.query.filter(Show.venue_id == self.id).filter(Show.start_time < datetime.datetime.now()).all()

    @property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)
    
    @property
    def past_shows_count(self):
        return len(self.past_shows)

artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)
    genres = db.relationship('Genre', secondary=artist_genres, lazy='subquery',
        backref=db.backref('artists', lazy=True))

    @property
    def upcoming_shows(self):
        return Show.query.filter(Show.artist_id == self.id).filter(Show.start_time >= datetime.datetime.now()).all()

    @property
    def past_shows(self):
        return Show.query.filter(Show.artist_id == self.id).filter(Show.start_time < datetime.datetime.now()).all()

    @property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)

    @property
    def past_shows_count(self):
        return len(self.past_shows)

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    @property
    def start_time_formatted(self):
        return self.start_time.strftime('%d %B %Y %H:%M')
