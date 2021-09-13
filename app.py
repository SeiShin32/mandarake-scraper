from re import template
from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
import psycopg2, os

app = Flask(__name__)
app.secret_key = os.urandom(24)

from user import user_routes
from link import link_routes


@app.route('/')
def home():
    con = psql_connection()
    cur = con.cursor()

    try:    
     cur.execute("SELECT * FROM (SELECT DISTINCT ON (name) name, price, to_char(date, 'dd/mm/yyyy HH24:MI'), date, link FROM price_info ORDER BY name, date DESC) t ORDER BY date DESC, price")
     records = cur.fetchall()
    except:
     records = []

    try:
     print(session['username'])
     username = session['username']
    except:
     username = 'Anon'
      
    con.close()

    return render_template('home.html', records=records, username=username)