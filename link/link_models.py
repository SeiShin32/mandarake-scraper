from re import template
from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
import psycopg2, os
from app import app
from scraper import scan_name, get_soup

class Link:
 
 def add_link(session):
    link = request.form["link"]
    print("\n" + link + "\n")
    print('user id: ' + str(session['id']) + "\n")

    if not link:
        print("Empty link!")
        return redirect(url_for('home'))

    con = psql_connection()
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS links(
    link_id serial PRIMARY KEY, link VARCHAR(255) NOT NULL
    )''')

    con.commit()

    check_query = "SELECT EXISTS(SELECT * FROM users_links WHERE user_id = %s AND link_id = (SELECT link_id FROM links WHERE link = %s))"
    cur.execute(check_query, (session['id'], link,))

    is_added = cur.fetchone()[0]

    if is_added:
        print("This user has already added this link!")
        con.close()
        return redirect(url_for('home'))

    exists_query = "SELECT EXISTS(SELECT 1 FROM links WHERE link = %s)"
    cur.execute(exists_query, (link,))
    
    is_link_exists = cur.fetchone()[0]

    if is_link_exists:
        insert_query = 'INSERT INTO users_links (user_id, link_id) VALUES (%s, (SELECT link_id FROM links WHERE link = %s))'
        cur.execute(insert_query, (session['id'], link,))
        con.commit()
        con.close()
        return redirect(url_for('home'))

    soup = get_soup(link)
    name = scan_name(soup, link)

    insert_query = 'INSERT INTO links (link, name) VALUES (%s, %s)'
    cur.execute(insert_query, (link, name,))

    con.commit()
    
    get_link_id = "SELECT link_id from links where link = %s"
    cur.execute(get_link_id, (link, ))
    link_id = cur.fetchone()
    print(link_id)

    insert_query = 'INSERT INTO users_links (link_id, user_id) VALUES (%s, %s)'
    cur.execute(insert_query, (link_id, session['id'],))    

    con.commit()
    
    print('Link has been added successfully')
    return redirect(url_for('home'))

 def delete_link(self, session):
    link = request.form["link"]
    
    if not link:
        print("Empty link!")       
        return redirect(url_for('home'))

    con = psql_connection()
    cur = con.cursor()

    check_query = "SELECT EXISTS(SELECT 1 FROM users_links where user_id = %s AND link_id = (SELECT link_id FROM links WHERE link = %s))"
    cur.execute(check_query, (session['id'], link,))

    is_added = cur.fetchone()[0]

    if is_added == 0:
        print("This user doesn't have this link added!")
        con.close()
        return redirect(url_for('home'))

    delete_query = 'DELETE FROM users_links WHERE user_id = %s AND link_id = (SELECT link_id FROM links WHERE link = %s)'
    cur.execute(delete_query, (session['id'], link,))
    con.commit()

    check_query = "SELECT EXISTS(SELECT * FROM users_links WHERE link_id = (SELECT link_id FROM links WHERE link = %s))"
    cur.execute(check_query, (link,))
    link_exists = cur.fetchone()[0]

    if link_exists == 0:
     delete_query = 'DELETE FROM links WHERE link = %s'
     cur.execute(delete_query, (link,))
     con.commit()
     con.close()
     return redirect(url_for('home'))  
       
    con.close()

    print("Record has been deleted")
    return redirect(url_for('home'))
