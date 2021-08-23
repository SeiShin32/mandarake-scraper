from re import template
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():


    con = sqlite3.connect('prices.db')
    cur = con.cursor()

    try:
     records = cur.execute('SELECT * FROM weekly_stats').fetchall()
    except Exception:
        records = []

    con.close()

    return render_template('home.html', records=records)