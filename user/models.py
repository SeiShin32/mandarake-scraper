from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
from passlib.hash import pbkdf2_sha256
import psycopg2

class User:
    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = user
        return user, 200

    def sign_up():            
        email = request.form["email"]
        name = request.form["name"]
        password = pbkdf2_sha256.encrypt(request.form["password"]) 

        with psql_connection() as con:
            cur = con.cursor()
            exists_query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"
            cur.execute(exists_query, (email,))
            check = cur.fetchone()[0]
            if check:
             print("This link already exists!")
             return 200 
                      
            insert_query = 'INSERT INTO users (email, name, password) VALUES (%s, %s, %s)'
            cur.execute(insert_query, (email, name, password,))
            con.commit()

        return print(email, name, password)