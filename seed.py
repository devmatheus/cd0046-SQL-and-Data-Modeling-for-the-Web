import datetime
import random
from sqlalchemy import func, text

from app_instance import app, db

with app.app_context():
    from models import State, City, Genre, Venue, Artist, Show

    # Clear all tables
    db.session.execute(text('DELETE FROM venue_genres'))
    db.session.execute(text('DELETE FROM artist_genres'))
    Show.query.delete()
    Artist.query.delete()
    Venue.query.delete()
    Genre.query.delete()
    City.query.delete()
    State.query.delete()

    states = [
        {"code": "AL", "name": "Alabama"},
        {"code": "AK", "name": "Alaska"},
        {"code": "AZ", "name": "Arizona"},
        {"code": "AR", "name": "Arkansas"},
        {"code": "CA", "name": "California"},
        {"code": "CO", "name": "Colorado"},
        {"code": "CT", "name": "Connecticut"},
        {"code": "DE", "name": "Delaware"},
        {"code": "FL", "name": "Florida"},
        {"code": "GA", "name": "Georgia"},
        {"code": "HI", "name": "Hawaii"},
        {"code": "ID", "name": "Idaho"},
        {"code": "IL", "name": "Illinois"},
        {"code": "IN", "name": "Indiana"},
        {"code": "IA", "name": "Iowa"},
        {"code": "KS", "name": "Kansas"},
        {"code": "KY", "name": "Kentucky"},
        {"code": "LA", "name": "Louisiana"},
        {"code": "ME", "name": "Maine"},
        {"code": "MD", "name": "Maryland"},
        {"code": "MA", "name": "Massachusetts"},
        {"code": "MI", "name": "Michigan"},
        {"code": "MN", "name": "Minnesota"},
        {"code": "MS", "name": "Mississippi"},
        {"code": "MO", "name": "Missouri"},
        {"code": "MT", "name": "Montana"},
        {"code": "NE", "name": "Nebraska"},
        {"code": "NV", "name": "Nevada"},
        {"code": "NH", "name": "New Hampshire"},
        {"code": "NJ", "name": "New Jersey"},
        {"code": "NM", "name": "New Mexico"},
        {"code": "NY", "name": "New York"},
        {"code": "NC", "name": "North Carolina"},
        {"code": "ND", "name": "North Dakota"},
        {"code": "OH", "name": "Ohio"},
        {"code": "OK", "name": "Oklahoma"},
        {"code": "OR", "name": "Oregon"},
        {"code": "PA", "name": "Pennsylvania"},
        {"code": "RI", "name": "Rhode Island"},
        {"code": "SC", "name": "South Carolina"},
        {"code": "SD", "name": "South Dakota"},
        {"code": "TN", "name": "Tennessee"},
        {"code": "TX", "name": "Texas"},
        {"code": "UT", "name": "Utah"},
        {"code": "VT", "name": "Vermont"},
        {"code": "VA", "name": "Virginia"},
        {"code": "WA", "name": "Washington"},
        {"code": "WV", "name": "West Virginia"},
        {"code": "WI", "name": "Wisconsin"},
        {"code": "WY", "name": "Wyoming"},
    ]

    for state in states:
        db.session.add(State(**state))

    cities = [
        {"name": "New York", "state_code": "NY"},
        {"name": "Los Angeles", "state_code": "CA"},
        {"name": "Chicago", "state_code": "IL"},
        {"name": "Houston", "state_code": "TX"},
        {"name": "Phoenix", "state_code": "AZ"},
        {"name": "Philadelphia", "state_code": "PA"},
        {"name": "San Antonio", "state_code": "TX"},
        {"name": "San Diego", "state_code": "CA"},
        {"name": "Dallas", "state_code": "TX"},
        {"name": "San Jose", "state_code": "CA"},
        {"name": "Austin", "state_code": "TX"},
        {"name": "Jacksonville", "state_code": "FL"},
        {"name": "Fort Worth", "state_code": "TX"},
        {"name": "Columbus", "state_code": "OH"},
        {"name": "San Francisco", "state_code": "CA"},
        {"name": "Charlotte", "state_code": "NC"},
        {"name": "Indianapolis", "state_code": "IN"},
        {"name": "Seattle", "state_code": "WA"},
        {"name": "Denver", "state_code": "CO"},
        {"name": "Washington", "state_code": "WA"},
        {"name": "Boston", "state_code": "MA"},
        {"name": "Nashville", "state_code": "TN"},
        {"name": "El Paso", "state_code": "TX"},
        {"name": "Detroit", "state_code": "MI"},
        {"name": "Memphis", "state_code": "TN"},
        {"name": "Portland", "state_code": "OR"},
        {"name": "Oklahoma City", "state_code": "OK"},
        {"name": "Las Vegas", "state_code": "NV"},
        {"name": "Louisville", "state_code": "KY"},
        {"name": "Baltimore", "state_code": "MD"},
        {"name": "Milwaukee", "state_code": "WI"},
        {"name": "Albuquerque", "state_code": "NM"},
        {"name": "Tucson", "state_code": "AZ"},
        {"name": "Fresno", "state_code": "CA"},
        {"name": "Sacramento", "state_code": "CA"},
        {"name": "Mesa", "state_code": "AZ"},
        {"name": "Atlanta", "state_code": "GA"}
    ]

    for city in cities:
        db.session.add(City(**city))

    genres = [
        "Pop",
        "Rock",
        "Hip Hop",
        "Rap",
        "Blues",
        "Jazz",
        "Classical",
        "Country",
        "R&B",
        "Soul",
        "Electronic",
        "Folk",
        "Reggae",
        "Metal",
        "Latin",
        "World",
        "Gospel",
        "Other"
    ]

    for genre in genres:
        db.session.add(Genre(name=genre))

    venues = [
        {
            "name": "The Fillmore",
            "city": "San Francisco",
            "address": "1805 Geary Blvd, San Francisco, CA 94115",
            "phone": "(415) 346-3000",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "facebook_link": "https://www.facebook.com/TheFillmoreSF/",
            "website": "https://www.fillmore.com/",
            "seeking_talent_description": "The Fillmore is seeking talented musicians in all genres to perform on our stage. We have a strong commitment to supporting local and emerging artists."
        },
        {
            "name": "The Bowery Ballroom",
            "city": "New York",
            "address": "6 Delancey St, New York, NY 10002",
            "phone": "(212) 533-2111",
            "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
            "facebook_link": "https://www.facebook.com/TheBoweryBallroom/",
            "website": "https://www.boweryballroom.com/",
            "seeking_talent_description": "The Bowery Ballroom is seeking talented musicians in all genres to perform on our stage. We have a passion for supporting independent and alternative artists."
        },
        {
            "name": "The Troubadour",
            "city": "Los Angeles",
            "address": "9081 Santa Monica Blvd, West Hollywood, CA 90069",
            "phone": "(310) 276-1158",
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "facebook_link": "https://www.facebook.com/TroubadourWestHollywood/",
            "website": "https://www.troubadour.com/",
            "seeking_talent_description": "The Troubadour is seeking talented musicians in all genres to perform on our stage. We have a commitment to promoting emerging and established artists alike."
        }
    ]

    for venue in venues:
        venue['city_id'] = City.query.filter_by(name=venue['city']).first().id
        venue['seeking_talent'] = True
        filtered_data = {k: v for k, v in venue.items() if k in Venue.__table__.columns}
        venue_model = Venue(**filtered_data)

        number_of_genres = random.randint(1, Genre.query.count())
        venue_model.genres = Genre.query.order_by(func.random()).limit(number_of_genres).all()

        db.session.add(venue_model)

    artists = [
        {
            "name": "John Legend",
            "city": "Los Angeles",
            "address": "123 Main St, Los Angeles, CA 90001",
            "phone": "(555) 123-4567",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "facebook_link": "https://www.facebook.com/johnlegend/",
            "website": "https://www.johnlegend.com/",
            "seeking_venue_description": "John Legend is seeking high-quality venues to perform his soulful R&B music. Ideal venues should have a capacity of 500 or more, excellent sound and lighting systems, and a commitment to supporting live music."
        },
        {
            "name": "Ed Sheeran",
            "city": "New York",
            "address": "456 Park Ave, New York, NY 10022",
            "phone": "(555) 789-1234",
            "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "facebook_link": "https://www.facebook.com/EdSheeranMusic/",
            "website": "https://www.edsheeran.com/",
            "seeking_venue_description": "Ed Sheeran is seeking high-quality venues to perform his pop and folk-inspired music. Ideal venues should have a capacity of 1000 or more, excellent sound and lighting systems, and a commitment to supporting live music."
        },
        {
            "name": "Billie Eilish",
            "city": "Los Angeles",
            "address": "789 Elm St, Los Angeles, CA 90001",
            "phone": "(555) 987-6543",
            "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "facebook_link": "https://www.facebook.com/billieeilish/",
            "website": "https://www.billieeilish.com/",
            "seeking_venue_description": "Billie Eilish is seeking high-quality venues to perform her unique brand of alternative pop music. Ideal venues should have a capacity of 1000 or more, excellent sound and lighting systems, and a commitment to supporting live music."
        }
    ]

    for artist in artists:
        artist['city_id'] = City.query.filter_by(name=artist['city']).first().id
        artist['seeking_venue'] = True
        filtered_data = {k: v for k, v in artist.items() if k in Artist.__table__.columns}
        artist_model = Artist(**filtered_data)

        number_of_genres = random.randint(1, Genre.query.count())
        artist_model.genres = Genre.query.order_by(func.random()).limit(number_of_genres).all()

        db.session.add(artist_model)
        db.session.flush()
        last_inserted_id = artist_model.id

        for i in range(random.randint(1, 4)):
            random_venue = Venue.query.order_by(func.random()).first()

            random_seconds = random.randint(0, 60 * 60 * 24 * 365) # 1 year
            random_date = datetime.datetime.now() + datetime.timedelta(seconds=random_seconds)

            db.session.add(Show(
                venue_id=random_venue.id,
                artist_id=last_inserted_id,
                start_time=random_date
            ))

    db.session.commit()
