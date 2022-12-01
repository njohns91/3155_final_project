from flask import render_template, Blueprint, session, redirect
from src.repositories.user_repository import user_repository_singleton
from src.repositories.listing_repository import listing_repository_singleton
from src.models.models import db, Listing, Person

router = Blueprint('profile', __name__, template_folder='templates')



@router.get('/profile')
def profile(): #person_id from current user session
    if 'person' not in session:
        return redirect('/') 
    person_id = session['person']['person_id']
    person_info = user_repository_singleton.person_info(person_id)
    user_listings = listing_repository_singleton.get_user_listings(person_id)
    return render_template('profile.html', Person=person_info, user_list=user_listings)