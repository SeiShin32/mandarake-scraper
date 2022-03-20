from os import link
import psycopg2
from psycopg2 import Error
from psql_con import psql_connection 


if __name__ == "__main__":

    con = psql_connection()
    cur = con.cursor

    cur.execute('''CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY, email VARCHAR(255) NOT NULL, 
    name VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS price_info(
    id serial PRIMARY KEY, link int REFERENCES links (link_id) on delete cascade,
    price VARCHAR(255) NOT NULL, date TIMESTAMPTZ DEFAULT Now()
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS links(
    link_id serial PRIMARY KEY, link VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL
    )''')

    cur.execute('''CREATE TABLE users_links(
    user_id int references users(user_id) ON DELETE CASCADE, 
    link_id int references links(link_id) ON DELETE CASCADE, 
    PRIMARY KEY(user_id, link_id));''')

    