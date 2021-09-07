from re import template
from flask import Flask, render_template, request, redirect, url_for
from psql_con import psql_connection
import psycopg2

app = Flask(__name__)


@app.route('/')
def home():
    con = psql_connection()
    cur = con.cursor()

    try:
        records = cur.execute('SELECT * FROM daily_records GROUP BY name ORDER BY MAX(date) DESC'
        ).fetchall()
    except Exception:
        records = []

    con.close()

    return render_template('home.html', records=records)


@app.route('/add', methods=['POST'])
def add_link():
    link = request.form["link"]

    con = psql_connection()
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS target_list(
    id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT NOT NULL
    )''')

    response = con.execute(
        "SELECT EXISTS(SELECT * FROM target_list WHERE link ='" + link + "');")
    check = response.fetchone()[0]

    if not link:
        print("Empty link!")
        con.close()
        return redirect("/")

    if check:
        print("This link already exists!")
        con.close()
        return redirect("/")

    insert = cur.execute(
        'INSERT OR REPLACE INTO target_list VALUES (NULL ,"{l}")'.format(
            l=link)
    )

    con.commit()
    con.close()

    print('Link has been added successfully')
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete_link():

    link = request.form["link"]
    con = psql_connection()
    cur = con.cursor()

    response = con.execute(
        "SELECT EXISTS(SELECT * FROM target_list WHERE link ='" + link + "');")
    check = response.fetchone()[0]

    if not link:
        print("Empty link!")
        con.close()
        return redirect("/")

    if check == 0:
        print("Invalid link!")
        con.close()
        return redirect("/")

    cur.execute("DELETE FROM target_list WHERE link ='" + link + "';")
    cur.execute("DELETE FROM weekly_stats WHERE link ='" + link + "';")

    con.commit()
    con.close()

    print("Record successfully deleted")
    return redirect("/")


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')


