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
        flash(f'Must include file for image', 'error')
        return redirect('/create_listing')
    
    if listing_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
        flash(f'File must be jpg, jpeg, png, or webp', 'error')
        return redirect('/create_listing')
    
    safe_filename = secure_filename(f'{person_id}-{listing_image.filename}')
    
    listing_image.save(os.path.join('static','listing_images', safe_filename))

    listing = Listing(person_id, item_description, item_name, item_cetegory, safe_filename, item_price, datetime.now())
    
    db.session.add(listing)
    db.session.commit()
    flash(f'Listing "{item_name}" was updated', 'success')
    return redirect('/market_place')

    
@router.get('/update_listing/<listing_id>')
def update(listing_id):
    if 'person' not in session:
        return redirect('/')
    
    post_to_update = Listing.query.get(listing_id)

    return render_template('update_listing.html', post_to_update = post_to_update)

@router.post('/update_listing/<listing_id>')
def update_item(listing_id):
    if 'person' not in session:
        return redirect('/')

    post_to_update = Listing.query.get(listing_id)
    
    post_to_update.listing_description = request.form.get('product_description')
    post_to_update.title = request.form.get('product_title')
    post_to_update.category = request.form.get('product_category')
    post_to_update.price = request.form.get('product_price')

    listing_image = request.files['product_image']
    
    if listing_image.filename == '':
        flash(f'Must include file for image', 'error')
        return redirect(f'/update_listing/{listing_id}')
    if listing_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
        flash(f'File must be jpg, jpeg, png, or webp', 'error')
        return redirect(f'/update_listing/{listing_id}')
    
    safe_filename = secure_filename(f'{post_to_update.person_id}-{listing_image.filename}')
    listing_image.save(os.path.join('static','listing_images', safe_filename))

    post_to_update.listing_image = safe_filename
    
    try:
        db.session.commit()
        flash(f'Listing "{post_to_update.title}" was updated', 'success')
        return redirect('/profile')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/update_listing/{listing_id}')
