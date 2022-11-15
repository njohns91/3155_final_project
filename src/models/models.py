from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.String, nullable = False)
    listing_description = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False)
    listing_image = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    

    owner_id = db.Column(db.Integer, \
        db.ForeignKey('person.person_id'), nullable=False)
    
    listing_user = db.relationship('Person', backref='listing_person')

    def __init__(self, listing_description: str, title: str, category: str, listing_image: str, price: int) -> None:
        self.listing_description = listing_description
        self.title = title
        self.category = category
        self.listing_image = listing_image
        self.price = price
        



class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    profile_image = db.Column(db.String, nullable = False)
    person_pass = db.Column(db.String, nullable = False)
    bio = db.Column(db.String, nullable = False)
    
    def __init__(self, first_name: str, last_name: str, email: str, profile_image: str, person_pass: str, bio: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_image = profile_image
        self.person_pass = person_pass
        self.bio = bio
    
        


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    date_posted = db.Column(db.String, nullable = False)
    contents = db.Column(db.String, nullable = False)

    poster_id = db.Column(db.Integer, \
        db.ForeignKey('person.person_id'), nullable=False)

    post_user = db.relationship('Person', backref='user_post')

    
    posts_comments_id = db.Column(db.Integer, \
        db.ForeignKey('listing.listing_id'), nullable=False)

    post_listing = db.relationship('Listing', backref='listed_post')