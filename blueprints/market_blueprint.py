from flask import render_template, request, redirect, flash, Blueprint, session, abort
from datetime import datetime
from src.repositories.user_repository import user_repository_singleton
from src.repositories.listing_repository import listing_repository_singleton
from src.repositories.comment_repository import comment_repository_singleton
from werkzeug.utils import secure_filename
import os
from src.models.models import db, Listing, Person, Comment
from forms import SearchForm

router = Blueprint('market', __name__, template_folder='templates')

@router.get('/market_place')
def market():
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    all_listings = listing_repository_singleton.get_all_listing()
    return render_template('market_place.html', market=all_listings, person_id=person_id)

@router.get('/listing_page/<listing_id>')
def listing_display(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    single_listing = listing_repository_singleton.specific_listing(listing_id)
    listing_comments = comment_repository_singleton.get_listing_comments(listing_id)

    if single_listing == None:
        flash("Listing does not exsit", "error")
        return redirect('/market_place')
    return render_template('listing_page.html', Listing=single_listing, person_id=person_id, comments= listing_comments)

@router.get('/create_listing')
def create():
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    return render_template('create_listing.html', person_id=person_id)

@router.post('/create_listing')
def create_item():
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    person_id = session['person']['person_id']

    if person_id == None or item_description == None or item_name ==None or item_cetegory ==None or item_price == None:
        return redirect('/create_listing')

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
    return redirect(f'/listing_page/{listing.listing_id}')

@router.get('/update_listing/<listing_id>')
def update(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    post_to_update = listing_repository_singleton.specific_listing(listing_id)
    user_person_id = session['person']['person_id']
    profile_of_listing = user_repository_singleton.person_info(post_to_update.person_id)

    #Ensure user is tyring to edit own listing
    isOwner = profile_of_listing.person_id == user_person_id
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')

    return render_template('update_listing.html', post_to_update = post_to_update, person_id=user_person_id)

@router.post('/update_listing/<listing_id>')
def update_item(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    post_to_update = listing_repository_singleton.specific_listing(listing_id)
    user_person_id = session['person']['person_id']

    if not post_to_update:
        flash("Post doesnt exist", "error")
        return redirect(f'/profile/{user_person_id}')

    profile_of_listing = user_repository_singleton.person_info(post_to_update.person_id)
    
    #Ensure user is tyring to edit own listing
    isOwner = profile_of_listing.person_id == user_person_id
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')
    
    post_to_update.listing_description = request.form.get('product_description')
    post_to_update.title = request.form.get('product_title')
    post_to_update.category = request.form.get('product_category')
    post_to_update.price = request.form.get('product_price')

    if post_to_update.person_id == '' or post_to_update.listing_description == '' or post_to_update.title =='' or post_to_update.category =='' or post_to_update.price == '':
        return redirect(f'/update_listing/{listing_id}')


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
        return redirect(f'/listing_page/{listing_id}')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/update_listing/{listing_id}')

@router.get('/delete_listing/<listing_id>')
def delete(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    post_to_delete = listing_repository_singleton.specific_listing(listing_id)
    user_person_id = session['person']['person_id']

    if not post_to_delete:
        flash("Post doesnt exist", "error")
        return redirect(f'/profile/{user_person_id}')

    profile_of_listing = user_repository_singleton.person_info(post_to_delete.person_id)

    #Ensure user is tyring to edit own listing
    isOwner = profile_of_listing.person_id == user_person_id
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')
    
    try:
        #Delete users comments
        listing_comments = comment_repository_singleton.get_listing_comments(listing_id)
        for comment in listing_comments:
            db.session.delete(comment)

        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Listing deleted successfully!', 'success')
        return redirect(f'/profile/{user_person_id}')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/profile/{user_person_id}')

@router.post('/create_comment/<listing_id>')
def create_comment(listing_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    if not listing_repository_singleton.specific_listing(listing_id):
        flash("Listing does not exsit", "error")
        return redirect('/market_place')

    text = request.form.get('text')
    person_id = session['person']['person_id']

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        try:
            comment = Comment(person_id, listing_id, datetime.now(), text)
            db.session.add(comment)
            db.session.commit()
            flash(f'Comment was created', 'success')
        except Exception as e:
            flash(f'{e}', 'error')

    return redirect(f'/listing_page/{listing_id}')

@router.get('/update_comment/<listing_id>/<comment_id>')
def update_comment_page(listing_id, comment_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    person_id = session['person']['person_id']
    single_listing = listing_repository_singleton.specific_listing(listing_id)
    listing_comments = comment_repository_singleton.get_listing_comments_sorted(listing_id)
    comment = comment_repository_singleton.get_single_comment(comment_id)

    if single_listing == None:
        flash("Listing does not exsit", "error")
        return redirect('/market_place')
    elif not comment:
        flash("Comment does not exist", category="error")
        return redirect(f'/listing_page/{listing_id}')
    elif  person_id != comment.person_id and person_id  != comment.listing_id:
        flash("You cannot update comment", category="error")
        return redirect(f'/listing_page/{listing_id}')
    return render_template('update_comment.html', Listing=single_listing, person_id=person_id, comments=listing_comments, comment_id=comment_id)

@router.post('/update_comment/<listing_id>/<comment_id>')
def update_comment(listing_id, comment_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    single_listing = listing_repository_singleton.specific_listing(listing_id)
    if single_listing == None:
        flash("Listing does not exsit", "error")
        return redirect('/market_place')

    comment = comment_repository_singleton.get_single_comment(comment_id)
    text = request.form.get('text')
    person_id = session['person']['person_id']

    if not comment:
        flash("Comment does not exist", category="error")
        return redirect(f'/listing_page/{listing_id}')
    elif  person_id != comment.person_id and person_id  != comment.listing_id:
        flash("You cannot update comment", category="error")
    elif not text:
        flash('Comment cannot be empty.', category='error')
    else:
        try:
            comment.content = text
            db.session.commit()
            flash(f'Comment was updated', 'success')
        except Exception as e:
            flash(f'{e}', 'error')
        
    return redirect(f'/listing_page/{listing_id}')

@router.get('/delete_comment/<listing_id>/<comment_id>')
def delete_comment(listing_id, comment_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')
    
    single_listing = listing_repository_singleton.specific_listing(listing_id)
    if single_listing == None:
        flash("Listing does not exsit", "error")
        return redirect('/market_place')

    comment = comment_repository_singleton.get_single_comment(comment_id)
    person_id = session['person']['person_id']

    if not comment:
        flash("Comment does not exist", category="error")
        return redirect(f'/listing_page/{listing_id}')
    elif  person_id != comment.person_id and person_id  != comment.listing_id:
        flash("You cannot delete comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(f'/listing_page/{comment.listing_id}')

@router.post('/search')
def search():
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/') 

    form = SearchForm()
    listings = listing_repository_singleton.get_all_listing()
    person_id = session['person']['person_id']

    if form.validate_on_submit():
        listing_searched = form.searched.data
        listings = listings.filter(Listing.title.ilike('%' + listing_searched + '%'))
        listings = listings.order_by(Listing.title).all()

        return render_template('search.html', form=form, searched = listing_searched, listings=listings, person_id=person_id)