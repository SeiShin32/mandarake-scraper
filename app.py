from re import template
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    con = sqlite3.connect('prices.db')
    cur = con.cursor()

    try:
     records = cur.execute('SELECT * FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'
     ).fetchall()
    except Exception:
        records = []

    con.close()

    return render_template('home.html', records=records)


@app.route('/', methods=['POST'])
def add_link():
    link = request.form["link"]

    con = sqlite3.connect('prices.db', timeout = 10)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS target_list(
    link TEXT PRIMARY KEY
    )''')

    insert = cur.execute(
    'INSERT OR REPLACE INTO target_list VALUES ("{l}")'.format(l = link)
    )

    con.commit()
    con.close()

    print('Link has been added successfully')   
    return render_template("home.html")
