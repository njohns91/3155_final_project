from src.models.models import Listing, Person, Comment, db
from datetime import datetime
from security import bcrypt
import os
from werkzeug.utils import secure_filename
from flask import session

def refresh_db():
    Comment.query.delete()
    Listing.query.delete()
    db.session.commit()

def create_person(testEmail, first = "TestFName", last = "TestLName", password="123123123"):

    hashed_bytes = bcrypt.generate_password_hash(password, int(os.getenv('BYCRYPT_ROUNDS')))
    hashed_password = hashed_bytes.decode('utf-8')

    test_person = Person(first, last, testEmail, None, hashed_password, None)
    db.session.add(test_person)
    db.session.commit()
    
    return test_person

def create_listing(person_id, item_description = "Test Listing Description", item_name = "Test Item Name", item_cetegory = "Other", item_price = '20.02', time = datetime.now()):

    image_name = "testImage.png"
    
    test_listing = Listing(person_id, item_description, item_name, item_cetegory, image_name, item_price, time)
    db.session.add(test_listing)
    db.session.commit()
    return test_listing

def create_comment(person_id, listing_id, text = "Test Comment" ,time = datetime.now()):
    test_comment = Comment(person_id, listing_id, time, text)
    db.session.add(test_comment)
    db.session.commit()
    return test_comment