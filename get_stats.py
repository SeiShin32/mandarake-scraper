from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import sqlite3

def get_links():

   sqliteConnection = sqlite3.connect('prices.db')
   cursor = sqliteConnection.cursor()

   sqlite_select_query = """SELECT * from target_list"""
   cursor.execute(sqlite_select_query)
   links = []
   for row in cursor: 
    links.append(row[0])
    

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
    name TEXT, price TEXT, link TEXT, date TEXT
 )''')

 cur.execute('''CREATE TABLE IF NOT EXISTS target_list(
    link TEXT PRIMARY KEY
 )''')

 insert = cur.execute(
    'INSERT INTO weekly_stats VALUES ("%s", "%s", "%s", "%s")' % (
       record['name'], record['price'], record['link'], record['date']
       )
 )

 insert = cur.execute(
    'INSERT OR REPLACE INTO target_list VALUES ("%s")' % (
       record['link']
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
 price = driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
 name = driver.find_element_by_xpath("//div[@class='subject']/h1").text
 

 print(name)
 print(price)
 print(datetime.now().strftime('%d/%m/%Y %H:%M'))
 print("\n")
 save_data(name, price, link)

driver.close()
