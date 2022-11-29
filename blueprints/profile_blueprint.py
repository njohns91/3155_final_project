from flask import render_template, Blueprint, session, redirect
from src.repositories.listing_repository import listing_repository_singleton
from src.models.models import db, Listing

router = Blueprint('profile', __name__, template_folder='templates')



@router.get('/profile')
def profile(): #person_id from current user session
    if 'person' not in session:
        return redirect('/') 
    #profile_listing = listing_repository_singleton.profile_listing(person_id)
    return render_template('profile.html') #Listing=profile_listing