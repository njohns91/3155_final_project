import os

from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv

from src.models.models import db, Listing
from security import bcrypt

from blueprints.session_blueprint import router as session_blueprint
from blueprints.market_blueprint import router as market_blueprint
from blueprints.profile_blueprint import router as profile_blueprint

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.secret_key= os.getenv('APP_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)

#Session Controllers
#Index, Login, Signup, Signout

app.register_blueprint(session_blueprint)

#Market Controllers
#Market, listings, C_listing, U_listing

app.register_blueprint(market_blueprint)

#Profile Controllers
#Profile

app.register_blueprint(profile_blueprint)