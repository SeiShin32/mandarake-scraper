from re import template
from flask import Flask, render_template, request, redirect, url_for, session
from psql_con import psql_connection
import psycopg2, os
from app import app
from link.link_models import Link

@app.route('/add', methods=['POST'])
def add_link():   
    return Link.add_link(session)    

@app.route('/delete', methods=['POST', 'GET'])
def delete():
  return Link().delete_link(session)
