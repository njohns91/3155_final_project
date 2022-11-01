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


@app.post('/')
def create_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    return redirect('/') ##needs to be updated to profile page when that implementation is added

@app.post('/')
def update_item():
    item_name = request.form.get('product_title')
    item_description = request.form.get('product_description')
    item_cetegory = request.form.get('product_category')
    item_price = request.form.get('product_price')
    return redirect('/') ##needs to be updated to profile page when that implementation is added