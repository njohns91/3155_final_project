from urllib import request
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users={}

@app.get('/')
def home():
    return render_template('login.html')

@app.post('/')
def loginPost():
    print("hello   ;ajskdlfjasdfj")
    email = request.form.get('loginEmail')
    password = request.form.get('loginPassword')
    if email == "" or password =="":
        print('hi')
        return redirect('/')
    print(password)
    users.update({email: password})
    return redirect('/')