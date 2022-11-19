from flask import render_template, Blueprint, session, redirect

from src.models.models import db

router = Blueprint('profile', __name__, template_folder='templates')



@router.get('/profile')
def profile():
    if 'person' not in session:
        return redirect('/')
    return render_template('profile.html')