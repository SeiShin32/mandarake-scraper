from re import template
from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
import psycopg2, os
app = Flask(__name__)
app.secret_key = os.urandom(24)


from user import routes
from user.models import User 

@app.route('/')
def home():
    con = psql_connection()
    cur = con.cursor()

    try:    
     cur.execute("SELECT * FROM (SELECT DISTINCT ON (name) name, price, to_char(date, 'dd/mm/yyyy HH24:MI'), date, link FROM price_stats ORDER BY name, date DESC) t ORDER BY date DESC, price")
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


@app.route('/add', methods=['POST'])
def add_link():
    link = request.form["link"]

    con = psql_connection()
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS target_list(
    id serial PRIMARY KEY, link VARCHAR(255) NOT NULL
    )''')

    con.commit()

    exists_query = "SELECT EXISTS(SELECT 1 FROM target_list WHERE link = %s)"
    cur.execute(exists_query, (link,))
    
    check = cur.fetchone()[0]

    if not link:
        print("Empty link!")
        con.close()
        return redirect("/")

    if check:
        print("This link already exists!")
        con.close()
        return redirect("/")

    insert_query = 'INSERT INTO target_list (link) VALUES (%s)'
    cur.execute(insert_query, (link,))

    con.commit()
    con.close()

    print('Link has been added successfully')
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete_link():

    link = request.form["link"]
    con = psql_connection()
    cur = con.cursor()

    exists_query = "SELECT EXISTS(SELECT 1 FROM target_list WHERE link = %s)"
    cur.execute(exists_query, (link,))
    
    check = cur.fetchone()[0]

    if not link:
        print("Empty link!")
        con.close()
        return redirect("/")

    if check == 0:
        print("Invalid link!")
        con.close()
        return redirect("/")

    delete_query = 'DELETE FROM target_list WHERE link = %s'
    cur.execute(delete_query, (link,))
    delete_query = 'DELETE FROM price_stats WHERE link = %s'
    cur.execute(delete_query, (link,))
    con.commit()
    
    con.close()

    print("Record has been deleted")
    return redirect("/")




