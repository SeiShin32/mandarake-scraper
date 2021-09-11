from re import template
from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
import psycopg2, os
from app import app

class Link:

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

 def delete_link(self):

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
