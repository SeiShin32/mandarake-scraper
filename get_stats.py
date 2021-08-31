from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import sqlite3, time

def get_links():

   sqliteConnection = sqlite3.connect('prices.db')
   cursor = sqliteConnection.cursor()

   sqlite_select_query = """SELECT * from target_list"""
   cursor.execute(sqlite_select_query)
   links = []
   for row in cursor: 
    links.append(row[1])    

   cursor.close()
   sqliteConnection.close()
   return links

def save_data(name, price, link):

 record = {       
        'name': name,
        'price': price,
        'link': link,
        'date': datetime.now().strftime('%d/%m/%Y %H:%M')        
    }

 con = sqlite3.connect('prices.db', timeout = 10)
 cur = con.cursor()

 cur.execute('''CREATE TABLE IF NOT EXISTS weekly_stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price TEXT, link TEXT, date TEXT
 )''')

 insert = cur.execute(
    'INSERT INTO weekly_stats VALUES (NULL, "%s", "%s", "%s", "%s")' % (
       record['name'], record['price'], record['link'], record['date']
       )
 )

 con.commit()
 con.close()

#Setting up webdriver
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path='./geckodriver', options=options)

#Getting data from every link

links = get_links()

for link in links:
 driver.get(link)
 time.sleep(0.5)
  
 if 'mandarake' in link:  
   try:
      price = driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
      name = driver.find_element_by_xpath("//div[@class='subject']/h1").text
      print(name + "\n" + price + "\n" + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
      save_data(name, price, link)
   except Exception:
      print("Couldn't scan mandarake page properly! Link: " + link)

 if 'suruga-ya' in link:
   try:
     name = driver.find_elements_by_xpath('//h1[@class="h1_title_product"]')[0].text
     price = driver.find_element_by_xpath("//span[@class='text-price-detail price-buy']").text
     price = ''.join(x for x in price if x.isdigit())
     print(name + "\n" + price + "\n" + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
     save_data(name, price, link)
   except Exception:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")
      

driver.close()
