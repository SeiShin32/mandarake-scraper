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
     print(session['username'])
     username = session['username']
    except:
     username = 'Anon'
     session['id'] = '0'

    try:
     records_query = '''select l.link, l.name, pi.price, 
     to_char(pi.date, 'dd/mm/yyyy HH24:MI') from users_links as ul inner join links l on ul.link_id = l.link_id 
     inner join (select distinct on (link_id) link_id, price, date from price_info order by link_id, date desc) pi 
     on pi.link_id = ul.link_id where ul.user_id = %s'''
     cur.execute(records_query, (session['id'], )) 
     records = cur.fetchall()
    except:
     records = []
      
    con.close()

    return render_template('home.html', records=records, username=username)