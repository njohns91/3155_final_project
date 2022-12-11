from flask import render_template, request, redirect, flash, Blueprint, session
from datetime import datetime
from src.repositories.listing_repository import listing_repository_singleton
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
import os
from src.models.models import db, Listing, Person, Comment
from forms import SearchForm

router = Blueprint('market', __name__, template_folder='templates')

@router.get('/market_place')
def market():
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    all_listings = listing_repository_singleton.get_all_listing()
    return render_template('market_place.html', market=all_listings, person_id=person_id)

@router.get('/listing_page/<listing_id>')
def listing_display(listing_id):
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    single_listing = listing_repository_singleton.specific_listing(listing_id)
    return render_template('listing_page.html', Listing=single_listing, person_id=person_id)

@router.get('/create_listing')
def create():
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    return render_template('create_listing.html', person_id=person_id)

@router.post('/create_listing')
def create_item():
    if 'person' not in session:
        return redirect('/')

    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    person_id = session['person']['person_id']
    
    #save listing images
    
    if 'product_image' not in request.files:
        return redirect('/create_listing')
    
    listing_image = request.files['product_image']
    
    if listing_image.filename == '':
        flash('Must include file for image', 'error')
        return redirect('/create_listing')
    
    if listing_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
        flash('File must be jpg, jpeg, png, or webp', 'error')
        return redirect('/create_listing')
    
    safe_filename = secure_filename(f'{person_id}-{listing_image.filename}')
    
    listing_image.save(os.path.join('static','listing_images', safe_filename))

    listing = Listing(person_id, item_description, item_name, item_cetegory, safe_filename, item_price, datetime.now())
    
    db.session.add(listing)
    db.session.commit()
    flash(f'Listing "{item_name}" was created', 'success')
    return redirect('/market_place')

@router.post('/create-comment/<listing_id>')
def create_comment(listing_id):
    if 'person' not in session:
        return redirect('/')
    
    text = request.form.get('text')
    person_id = session['person']['person_id']

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        comment = Comment(person_id, listing_id, datetime.now(), text)
        db.session.add(comment)
        db.session.commit()
        
    return redirect(f'/listing_page/{listing_id}')

@router.get('/delete-comment/<comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.filter_by(comment_id = comment_id).first()
    person_id = session['person']['person_id']

    if not comment:
        flash("Comment does nto exist", category="error")
    elif  person_id != comment.person_id and person_id  != comment.listing_id:
        flash("You cannot delete comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
    
        
    return redirect(f'/market_place')

@router.get('/update_listing/<listing_id>')
def update(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    post_to_update = Listing.query.get(listing_id)
    user_person_id = session['person']['person_id']
    profile_of_listing = Person.query.get(post_to_update.person_id)

    #Ensure user is tyring to edit own listing
    isOwner = profile_of_listing.person_id == user_person_id
    print(isOwner, profile_of_listing.person_id, user_person_id)
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')

    return render_template('update_listing.html', post_to_update = post_to_update, person_id=user_person_id)

@router.post('/update_listing/<listing_id>')
def update_item(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    post_to_update = Listing.query.get(listing_id)
    user_person_id = session['person']['person_id']
    profile_of_listing = Person.query.get(post_to_update.person_id)

    #Ensure user is tyring to edit own listing
    isOwner = profile_of_listing.person_id == user_person_id
    print(isOwner, profile_of_listing.person_id, user_person_id)
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')
    
    post_to_update.listing_description = request.form.get('product_description')
    post_to_update.title = request.form.get('product_title')
    post_to_update.category = request.form.get('product_category')
    post_to_update.price = request.form.get('product_price')

    listing_image = request.files['product_image']    
    if listing_image.filename != '':
        if listing_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
            flash('File must be jpg, jpeg, png, or webp', 'error')
            return redirect(f'/update_listing/{listing_id}')    
        safe_filename = secure_filename(f'{post_to_update.person_id}-{listing_image.filename}')
        listing_image.save(os.path.join('static','listing_images', safe_filename))
        post_to_update.listing_image = safe_filename
    
    try:
        db.session.commit()
        flash(f'Listing "{post_to_update.title}" was updated', 'success')
        return redirect(f'/profile/{user_person_id}')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/update_listing/{listing_id}')

@router.get('/delete_listing/<listing_id>')
def delete(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    post_to_delete = Listing.query.get(listing_id)
    user_person_id = session['person']['person_id']
    profile_of_listing = Person.query.get(post_to_delete.person_id)

    #Ensure user is tyring to edit own listing
    isOwner = profile_of_listing.person_id == user_person_id
    print(isOwner, profile_of_listing.person_id, user_person_id)
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')
    
    post_to_delete.listing_description = request.form.get('product_description')
    post_to_delete.title = request.form.get('product_title')
    post_to_delete.category = request.form.get('product_category')
    post_to_delete.price = request.form.get('product_price')

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Listing deleted successfully!', 'success')
        return redirect(f'/profile/{user_person_id}')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/profile/{user_person_id}')

@router.post('/search')
def search():
    if 'person' not in session:
        return redirect('/') 

    form = SearchForm()
    listings = Listing.query
    person_id = session['person']['person_id']

    if form.validate_on_submit():
        listing_searched = form.searched.data
        listings = listings.filter(Listing.title.ilike('%' + listing_searched + '%'))
        listings = listings.order_by(Listing.title).all()

        return render_template('search.html', form=form, searched = listing_searched, listings=listings, person_id=person_id)