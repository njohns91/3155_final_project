from flask import render_template, request, redirect, flash, Blueprint, session
from datetime import datetime

from src.models.models import db, Listing

router = Blueprint('market', __name__, template_folder='templates')



@router.get('/market_place')
def market():
    if 'person' not in session:
        return redirect('/')
    return render_template('market_place.html')

@router.get('/listing_page')
def listing():
    if 'person' not in session:
        return redirect('/')
    return render_template('listing_page.html')

@router.get('/create_listing')
def create():
    if 'person' not in session:
        return redirect('/')
    return render_template('create_listing.html')

@router.post('/create_listing')
def create_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    item_image = request.form.get('product_image')
    person_id = session['person']['person_id']

    print(person_id)

    listing = Listing(person_id, item_description, item_name, item_cetegory, item_image, item_price, datetime.now())
    db.session.add(listing)
    db.session.commit()
    return redirect('/market_place')

@router.get('/update_listing')
def update():
    if 'person' not in session:
        return redirect('/')
    return render_template('update_listing.html')

@router.post('/update_listing')
def update_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    return redirect('/profile')
