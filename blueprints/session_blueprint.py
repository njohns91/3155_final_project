import os

from flask import render_template, request, redirect, flash, Blueprint, session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from src.models.models import db, Person
from security import bcrypt

load_dotenv()

router = Blueprint('session', __name__, template_folder='templates')



@router.get('/')
def home():
    if 'person' in session:
        return redirect('/market_place')
    return render_template('index.html')

@router.get('/login')
def login():
    if 'person' in session:
        return redirect('/market_place')
    return render_template('login.html')

@router.post('/login')
def loginPost():
    email = request.form.get("loginEmail")
    password = request.form.get('loginPassword')

    user = Person.query.filter_by(email=email).first()

    if not user:
        flash(u'Account with associated email does not exsit', 'error')
        return redirect('/login')

    #Password Validation
    valid = bcrypt.check_password_hash(user.person_pass, password)

    if valid:
        session['person'] = {
            'person_id':user.person_id
        }
        flash(u'You were successfully logged in', 'success')
        return redirect('/market_place')
    else:
        flash(u'Incorrect password', 'error')
        return redirect('/login')

@router.get('/signup')
def signup():
    if 'person' in session:
        return redirect('/market_place')
    return render_template('signup.html')

@router.post('/signup')
def signupPost():
    first = request.form.get("signupFirst")
    last = request.form.get("signupLast")
    email = request.form.get("signupEmail")
    password = request.form.get('signupPassword')

    #Hashing Password
    hashed_bytes = bcrypt.generate_password_hash(password, int(os.getenv('BYCRYPT_ROUNDS')))
    hashed_password = hashed_bytes.decode('utf-8')

    person = Person(first, last, email, None, hashed_password, None)

    db.session.add(person)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash(u'An account with that email already exsits', 'error')
        return redirect('/signup')

    flash(u'Your account was successfully created', 'success')
    return redirect('/login')

@router.get('/signout')
def signout():
    if 'person' not in session:
        return redirect('/')
    session.pop('person')
    return redirect('/')

