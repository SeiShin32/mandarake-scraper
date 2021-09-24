from os import getloadavg
from bs4 import BeautifulSoup
from datetime import datetime
from psql_con import psql_connection
import psycopg2, time, requests

def get_soup(link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(link, headers = headers)
    return BeautifulSoup(page.text, "html.parser")

def get_links():
        con = psql_connection()
        cur = con.cursor()
        cur.execute('SELECT link_id, link from links')
        links = []
        for row in cur:
            links.append(row)
        
        cur.close()
        con.close()
        return links

def save_data(link_id, price):

        record = {
            'price': price,
        }

        con = psql_connection()
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS price_info(
        id serial PRIMARY KEY, link int REFERENCES links (link_id) on delete cascade, price VARCHAR(255) NOT NULL, date TIMESTAMPTZ DEFAULT Now()
        )''')

        con.commit()

        insert_query = "INSERT INTO price_info (link_id, price) VALUES (%s, %s)"
        cur.execute(insert_query, (link_id, record['price'], ))

        con.commit()
        con.close()
 

def scan_name(soup, link):

 if 'mandarake' in link:
  try:
      name = soup.find(itemprop='name').get('content')
      print(name + "\n")
      return name 
  except TypeError:
      print("Couldn't scan mandarake page properly! Link: " + link)
     
 if 'suruga-ya' in link:
  try:
        name = soup.select('h1.h1_title_product')[0].text.strip()
        print(name + "\n")  
        return name 
  except TypeError:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")

 if 'mercari' in link:
  try:
      name = soup.select('h1.item-name')[0].text.strip()
      print("\n" + name + "\n")
      return name
  except TypeError:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")
    

def scan_price(soup, link):
  
 if 'mandarake' in link:
  try:
      price = soup.find(itemprop='price').get('content')
      print("\n" + price + "\n")
      return price                
  except TypeError:
      print("Couldn't scan mandarake page properly! Link: " + link)
     
 if 'suruga-ya' in link:
  try:
      price = soup.find('span', class_='text-price-detail price-buy').text
      price = ''.join(x for x in price if x.isdigit())
      print("\n" + price + "\n")
      return price
  except TypeError:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")

 if 'mercari' in link:
  try:
      price = soup.find('span', class_='item-price bold').text
      price = ''.join(x for x in price if x.isdigit())
      print("\n" + price + "\n")
      return price
  except TypeError:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")
     
if __name__ == "__main__":
  links = get_links()
  
  for link in links:
    try:
        print(link[0])
        save_data(link[0], scan_price(get_soup(link[1]), link[1]))
    except:
       print("Something appears to be wrong with the link!" + '\n' + str(link)) 
  
 
     



