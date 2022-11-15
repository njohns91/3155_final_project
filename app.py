from urllib import request
from flask import Flask, render_template, request, redirect
from models import db, Person, Listing


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Butter2002!@localhost:5432/Final'

db.init_app(app)



users={}

@app.get('/')
def home():
    return render_template('login.html') ## Currently set to listing/market page 

@app.get('/profile')
def profile():
    return render_template('profile.html')

@app.post('/')
def loginPost():
    email = request.form.get("loginEmail")
    password = request.form.get('loginPassword')
    users.update({email: password})
    return redirect('/market_place') ##needs to be updated to marketplace page when that implementation is added

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