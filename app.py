from re import template
from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/add', methods=['POST'])
def add_link():
    link = request.form["link"]
    if not ("mandarake") in link:
        print("Invalid link!")
        return redirect("/")

    con = sqlite3.connect('prices.db', timeout = 10)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS target_list(
    id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT NOT NULL
    )''')

    insert = cur.execute(
    'INSERT OR REPLACE INTO target_list VALUES (NULL ,"{l}")'.format(l = link)
    )

    con.commit()
    con.close()

    print('Link has been added successfully')   
    return redirect("/")

@app.route("/delete", methods = ["POST"])  
def deletelink():  

    link = request.form["link"]  
    con = sqlite3.connect("prices.db")     
    cur = con.cursor()
    cur.execute("DELETE FROM target_list WHERE link ='"+ link +"';")
    cur.execute("DELETE FROM weekly_stats WHERE link ='"+ link +"';")

    con.commit()
    con.close()

    print("record successfully deleted") 
    return redirect("/")