from os import link
import psycopg2
from psycopg2 import Error


def psql_connection():
 return psycopg2.connect(user="xxx",
 password="xxx",
 host="127.0.0.1",
 port="5432",
 database="xxx")