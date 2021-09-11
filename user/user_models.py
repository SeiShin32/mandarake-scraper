from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
from passlib.hash import pbkdf2_sha256
import psycopg2

class User:
    def sign_up():
        msg = ' '

        user = {
            'email': '',
         'username': '',
         'password': ''
        }
     
        if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
         user['email'] = request.form['email']
         user['username'] = request.form['name']
         user['password'] = request.form['password']
         with psql_connection() as con:
            cur = con.cursor()
            exists_query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"
            cur.execute(exists_query, (user['email'],))
            check = cur.fetchone()[0]
            if check:
             msg = "This email is already taken!"
             return render_template('signup.html', msg=msg)  
                      
            insert_query = 'INSERT INTO users (email, name, password) VALUES (%s, %s, %s)'
            cur.execute(insert_query, (user['email'], user['username'], user['password'],))
            con.commit()
            return redirect('/')

        return render_template('signup.html', code=200)
    
    def login(self):
         msg = ' '
         
         if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
          email = request.form['email']
          password = request.form['password']
          with psql_connection() as con:
           cur = con.cursor()
           try:
            exists_query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cur.execute(exists_query, (email, password,))
            account = cur.fetchone()
            print(account)
            print(account[0])
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            return redirect('/'), session
           except:
            msg = 'Incorrect email/password!'
            return render_template('login.html', msg=msg)

         return render_template('login.html', msg=msg)

    def sign_out(self):
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('home'))
