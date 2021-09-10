from flask import Flask, request
from flask.templating import render_template
from werkzeug.utils import redirect
from app import app
from user.models import User
from psql_con import psql_connection

@app.route('/user/signup/', methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        try:
         User.sign_up()
        finally:
         render_template('signup.html') 
    return render_template('signup.html')

@app.route('/user/signout/')
def sign_out():
  return User().sign_out()

@app.route('/user/login/', methods=['POST'])
def login():
  return User().login()