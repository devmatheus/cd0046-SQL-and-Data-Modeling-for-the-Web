import re
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, ValidationError
from wtforms.validators import DataRequired, URL
from sqlalchemy import exists
from app_instance import app

def states_options():
    with app.app_context():
        from models import State, City
        return [(state.code, state.name) for state in State.query.filter(exists().where(City.state_code == State.code)).order_by(State.name).all()]

def genres_options():
    with app.app_context():
        from models import Genre
        return [(genre.id, genre.name) for genre in Genre.query.order_by(Genre.name).all()]

def validate_phone(form, field):
    phone_pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    if not phone_pattern.match(field.data):
        raise ValidationError('Invalid phone number')

def validate_state(form, field):
    with app.app_context():
        from models import State
        if not State.query.filter_by(code=field.data).first():
            raise ValidationError('Invalid state')

def validate_city(form, field):
    with app.app_context():
        from models import City
        if not City.query.filter_by(name=field.data, state_code=form.state.data).first():
            raise ValidationError('Invalid city')

def validate_genres(form, field):
    with app.app_context():
        from models import Genre
        if not Genre.query.filter(Genre.id.in_(field.data)).first():
            raise ValidationError('Invalid genres')

class ShowForm(Form):
    with app.app_context():
        from models import Artist, Venue

        artist_id = SelectField(
            'artist_id',
            choices=[(artist.id, artist.name) for artist in Artist.query.order_by(Artist.name).all()],
        )
        venue_id = SelectField(
            'venue_id',
            choices=[(venue.id, venue.name) for venue in Venue.query.order_by(Venue.name).all()],
        )
        start_time = StringField(
            'start_time',
            validators=[DataRequired()],
            default=datetime.today().strftime('%Y-%m-%d %H:%M')
        )

class ArtistForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            validate_state
        ],
        choices=states_options()
    )
    city = SelectField(
        'city',
        validators=[
            DataRequired(),
            validate_city
        ]
    )
    phone = StringField(
        'phone',
        validators=[validate_phone]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(),
            validate_genres
        ],
        choices=genres_options()
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[URL()]
    )
    website_link = StringField(
        'website_link',
        validators=[URL()]
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description'
    )

class VenueForm(Form):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    city = SelectField(
        'city',
        validators=[
            DataRequired(),
            validate_city
        ]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            validate_state
        ],
        choices=states_options()
    )
    address = StringField(
        'address',
        validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(),
            validate_genres
        ],
        choices=genres_options()
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[URL()]
    )
    website_link = StringField(
        'website_link',
        validators=[URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = StringField(
        'seeking_description'
    )
