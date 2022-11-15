from urllib import request
from flask import Flask, render_template, request, redirect, flash
from src.models.models import db, Person, Listing
from sqlalchemy.exc import IntegrityError
from datetime import datetime


app = Flask(__name__)
app.secret_key='12345'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Charl0tte_isc00l@localhost:5432/Final'

db.init_app(app)

users={}

#Account Controllers
#Index, Login, Signup, Signout

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.post('/login')
def loginPost():
    email = request.form.get("loginEmail")
    password = request.form.get('loginPassword')

    user = Person.query.filter_by(email=email).first()

    if(not user):
        flash(u'Account with associated email does not exsit', 'error')
        return redirect('/login')

    if (user.person_pass == password):
        flash(u'You were successfully logged in', 'success')
        return redirect('/market_place')
    else:
        flash(u'Incorrect password', 'error')
        return redirect('/login')

@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.post('/signup')
def signupPost():
    first = request.form.get("signupFirst")
    last = request.form.get("signupLast")
    email = request.form.get("signupEmail")
    password = request.form.get('signupPassword')

    person = Person(first, last, email, None, password, None)
    db.session.add(person)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(u'An account with that email already exsits', 'error')
        return redirect('/signup')

    flash(u'Your account was successfully created', 'success')
    return redirect('/login')

@app.get('/signout')
def signout():
    return redirect('/')


#Market Controllers
#Market, listings, C_listing, U_listing

@app.get('/market_place')
def market():
    return render_template('market_place.html')

@app.get('/listing_page')
def listing():
    return render_template('listing_page.html')

@app.get('/create_listing')
def create():
    return render_template('create_listing.html')

@app.post('/create_listing')
def create_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    item_image = request.form.get('product_image')

    print(datetime.now())

    listing = Listing(item_description, item_name, item_cetegory, item_image, item_price, datetime.now())
    db.session.add(listing)
    db.session.commit()
    return redirect('/market_place')

@app.get('/update_listing')
def update():
    return render_template('update_listing.html')

@app.post('/update_listing')
def update_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    return redirect('/profile')


#Profile Controllers
#Profile

@app.get('/profile')
def profile():
    return render_template('profile.html')