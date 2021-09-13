from re import template
from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
import psycopg2, os
from app import app
from scraper import scan_name, get_driver

class Link:

 def add_link():
    link = request.form["link"]
    print("\n" + link + "\n")

    con = psql_connection()
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS links(
    link_id serial PRIMARY KEY, link VARCHAR(255) NOT NULL
    )''')

    con.commit()

    exists_query = "SELECT EXISTS(SELECT 1 FROM links WHERE link = %s)"
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

    driver = get_driver()
    name = scan_name(driver, link)

    insert_query = 'INSERT INTO links (link, name) VALUES (%s, %s)'
    cur.execute(insert_query, (link, name,))

    con.commit()
    

    print('Link has been added successfully')
    return redirect("/")

 def delete_link(self):

    link = request.form["link"]
    con = psql_connection()
    cur = con.cursor()

    exists_query = "SELECT EXISTS(SELECT 1 FROM links WHERE link = %s)"
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

    delete_query = 'DELETE FROM links WHERE link = %s'
    cur.execute(delete_query, (link,))
    delete_query = 'DELETE FROM price_info WHERE link = %s'
    cur.execute(delete_query, (link,))
    con.commit()
    
    con.close()

    print("Record has been deleted")
    return redirect("/")
