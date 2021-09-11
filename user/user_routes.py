from flask import Flask, request
from flask.templating import render_template
from werkzeug.utils import redirect
from app import app
from user.user_models import User
from psql_con import psql_connection

@app.route('/user/signup/', methods=["POST", "GET"])
def sign_up():   
    return User.sign_up()    

@app.route('/user/login/', methods=['POST', 'GET'])
def login():
  return User().login()       

@app.route('/user/signout/', methods=['GET'])
def sign_out():
  return User().sign_out()

