from flask import render_template, Blueprint, session, redirect, request, flash
from src.repositories.user_repository import user_repository_singleton
from src.repositories.listing_repository import listing_repository_singleton
from src.models.models import db, Listing, Person
import os
from werkzeug.utils import secure_filename
from security import bcrypt

router = Blueprint('profile', __name__, template_folder='templates')

@router.get('/profile')
def profile(): #person_id from current user session
    if 'person' not in session:
        return redirect('/') 
    person_id = session['person']['person_id']
    person_info = user_repository_singleton.person_info(person_id)
    user_listings = listing_repository_singleton.get_user_listings(person_id)
    return render_template('profile.html', Person=person_info, user_list=user_listings)

#Update Profile

@router.get('/update_profile/<person_id>')
def update_profile(person_id):
    if 'person' not in session:
        return redirect('/')
    profile_to_update = Person.query.get(person_id)
    return render_template('update_profile.html', profile_to_update = profile_to_update)

@router.post('/update_profile/<person_id>')
def updates_profile(person_id):
    if 'person' not in session:
        return redirect('/')
    
    profile_to_update = Person.query.get(person_id)

    profile_to_update.first_name = request.form.get('updateFirst')
    profile_to_update.last_name = request.form.get('updateLast')
    
    #Password Hashing
    passw = request.form.get('updatePassword')
    profile_to_update.password = ''
    if passw != '':
        hashed_bytes = bcrypt.generate_password_hash(passw, int(os.getenv('BYCRYPT_ROUNDS')))
        profile_to_update.person_pass = hashed_bytes.decode('utf-8')
    

    profile_image = request.files['updatePicture']
    
    if profile_image.filename != '':
        if  profile_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
            flash(f'File must be jpg, jpeg, png, or webp', 'error')
            return redirect(f'/update_profile/{person_id}')
        
        safe_filename = secure_filename(f'{profile_to_update.person_id}-{profile_image.filename}')
        profile_image.save(os.path.join('static','profile_images', safe_filename))

        profile_to_update.profile_image = safe_filename

    try:
        db.session.commit()
        flash("Profile Updated", 'success')
        return redirect('/profile')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/update_profile/{person_id}')

@router.get('/delete_profile/<person_id>')
def delete(person_id):
    if 'person' not in session:
        return redirect('/')
    profile_to_delete = Person.query.get(person_id)

    user_listings = listing_repository_singleton.get_user_listings(person_id)
    
    for listing in user_listings:
        db.session.delete(listing)

    db.session.commit()
    
    try:
        db.session.delete(profile_to_delete)
        db.session.commit()
        session.clear()
        flash('Listing deleted successfully!', 'success')
        return redirect('/')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect('/profile')