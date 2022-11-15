from urllib import request
from flask import Flask, render_template, request, redirect
from models import db, Person, Listing


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Butter2002!@localhost:5432/Final'

db.init_app(app)



users={}

@app.get('/')
def home():
    return render_template('login.html')

@app.get('/profile')
def profile():
    return render_template('profile.html')

@app.post('/')
def loginPost():
    email = request.form.get("loginEmail")
    password = request.form.get('loginPassword')

    person = Person('Seth', 'Seth', email, "Hello", password, "Testing bio")
    db.session.add(person)
    db.session.commit()
    return redirect('market_place.html') ##needs to be updated to marketplace page when that implementation is added

    
    



@app.post('/create_listing')
def create_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')

    listing = Listing(item_description, item_name, item_cetegory, None, item_price)
    db.session.add(listing)
    db.session.commit()
    return redirect('/') ##needs to be updated to profile page when that implementation is added


@app.post('/update_listing')
def update_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    return redirect('/profile')

@app.get('/market_place')
def market():
    return render_template('market_place.html')

@app.get('/signout')
def signout():
    return redirect('/')

@app.get('/create_listing')
def create():
    return render_template('create_listing.html')

@app.get('/update_listing')
def update():
    return render_template('update_listing.html')

@app.get('/listing_page')
def listing():
    return render_template('listing_page.html')