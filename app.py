from urllib import request
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users={}

@app.get('/')
def home():
    return render_template('login.html')

@app.post('/')
def loginPost():
    email = request.form.get("loginEmail")
    password = request.form.get('loginPassword')
    users.update({email: password})
    return redirect('/') ##needs to be updated to marketplace page when that implementation is added