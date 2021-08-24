from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import sqlite3

def get_link():
   link = "https://order.mandarake.co.jp/order/detailPage/item?itemCode=1172309839&ref=list&categoryCode=11&keyword=%E3%83%A8%E3%82%B3%E3%83%8F%E3%83%9E"
   return link

def save_data(name, price, link):

 record = {       
        'name': name,
        'price': price,
        'link': link,
        'date': datetime.now().strftime('%d/%m/%Y %H:%M')        
    }

 con = sqlite3.connect('prices.db')
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

#Getting data
driver.get(get_link())
price = driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
name = driver.find_element_by_xpath("//div[@class='subject']/h1").text
driver.close()

print(name)
print(price)
print(datetime.now().strftime('%d/%m/%Y %H:%M'))
save_data(name, price, get_link())