from flask import render_template, request, redirect, flash, Blueprint, session
from datetime import datetime
from src.repositories.listing_repository import listing_repository_singleton
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
import os
from src.models.models import db, Listing

router = Blueprint('market', __name__, template_folder='templates')



@router.get('/market_place')
def market():
    if 'person' not in session:
        return redirect('/')
    all_listings = listing_repository_singleton.get_all_listing()
    return render_template('market_place.html', market=all_listings)

@router.get('/listing_page')
def listing():
    if 'person' not in session:
        return redirect('/')
    return render_template('listing_page.html')


@router.get('/listing_page/<listing_id>')
def listing_display(listing_id):
    single_listing = listing_repository_singleton.specific_listing(listing_id)
    return render_template('listing_page.html', Listing=single_listing)



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
    person_id = session['person']['person_id']

    print(person_id)
    
    #save listing images
    
    if 'product_image' not in request.files:
        return redirect('/create_listing')
    
    listing_image = request.files['product_image']
    
    if listing_image.filename == '':
        return redirect('/create_listing')
    
    if listing_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
        return redirect('/create_listing')
    
    safe_filename = secure_filename(f'{person_id}-{listing_image.filename}')
    
    listing_image.save(os.path.join('static','listing_images', safe_filename))

    listing = Listing(person_id, item_description, item_name, item_cetegory, safe_filename, item_price, datetime.now())
    
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
