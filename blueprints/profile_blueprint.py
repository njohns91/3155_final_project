from flask import render_template, Blueprint, session, redirect, request, flash
from src.repositories.user_repository import user_repository_singleton
from src.repositories.listing_repository import listing_repository_singleton
from src.repositories.comment_repository import comment_repository_singleton
from src.models.models import db, Person, Comment
import os
from werkzeug.utils import secure_filename
from security import bcrypt

router = Blueprint('profile', __name__, template_folder='templates')

@router.get('/profile/<person_id>')
def profile(person_id): #person_id from current user session
    if 'person' not in session:
        return redirect('/')

    profile_person_info = user_repository_singleton.person_info(person_id)
    user_listings = listing_repository_singleton.get_user_listings(person_id)
    
    #Determines if user is going to own profile or someone elses
    user_person_id = session['person']['person_id']
    isOwner = profile_person_info.person_id == user_person_id

    return render_template('profile.html', Person=profile_person_info, user_list=user_listings, person_id=user_person_id, isOwner = isOwner)

#Update Profile
@router.get('/update_profile/<person_id>')
def update_profile(person_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    user_person_id = session['person']['person_id']
    profile_to_update = user_repository_singleton.person_info(person_id)

    #Ensure user is tyring to edit own account
    isOwner = profile_to_update.person_id == user_person_id
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')

    return render_template('update_profile.html', profile_to_update = profile_to_update, person_id=user_person_id)

@router.post('/update_profile/<person_id>')
def updates_profile(person_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    user_person_id = session['person']['person_id']
    profile_to_update = user_repository_singleton.person_info(person_id)

    #Ensure user is tyring to edit own account
    isOwner = profile_to_update.person_id == user_person_id
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')

    profile_to_update.first_name = request.form.get('updateFirst')
    profile_to_update.last_name = request.form.get('updateLast')
    profile_to_update.bio = request.form.get('updateBio')
    
    #Password Hashing
    passw = request.form.get('updatePassword')
    profile_to_update.password = ''
    if passw != '':
        hashed_bytes = bcrypt.generate_password_hash(passw, int(os.getenv('BYCRYPT_ROUNDS')))
        profile_to_update.person_pass = hashed_bytes.decode('utf-8')
    
    #Get profile picture and store it
    profile_image = request.files['updatePicture']
    
    if profile_image.filename != '':
        if  profile_image.filename.rsplit('.',1)[1].lower() not in ['jpg', 'jpeg', 'png', 'webp']:
            flash(f'File must be jpg, jpeg, png, or webp', 'error')
            return redirect(f'/update_profile/{person_id}')
        
        safe_filename = secure_filename(f'{profile_to_update.person_id}-{profile_image.filename}')
        profile_image.save(os.path.join('static','profile_images', safe_filename))

        profile_to_update.profile_image = safe_filename

    try:
        #Update profile
        db.session.commit()
        flash("Profile Updated", 'success')
        return redirect(f'/profile/{user_person_id}')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/update_profile/{person_id}')

@router.get('/delete_profile/<person_id>')
def delete(person_id):
    #Ensure user is logged in
    if 'person' not in session:
        return redirect('/')

    user_person_id = session['person']['person_id']
    profile_to_delete = user_repository_singleton.person_info(person_id)

    #Ensure user is tyring to edit own account
    isOwner = profile_to_delete.person_id == user_person_id
    if not isOwner:
        flash("Unathorized access", "error")
        return redirect(f'/profile/{user_person_id}')

    try:
        #Delete users comments
        user_comments = comment_repository_singleton.get_user_comments(person_id)
        for comment in user_comments:
            db.session.delete(comment)

        #Delete users listings
        user_listings = listing_repository_singleton.get_user_listings(person_id)
        for listing in user_listings:
            db.session.delete(listing)

        #Delete user
        db.session.delete(profile_to_delete)

        #Commit to database
        db.session.commit()
        session.clear()
        flash('Profile deleted successfully!', 'success')
        return redirect('/')
    except Exception as e:
        flash(f'{e}', 'error')
        return redirect(f'/profile/{user_person_id}')