from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import sqlite3


def save_data(name, price):

 record = {       
        'name': name,
        'price': price,
        'date': datetime.now().strftime('%-d %b %Y')
    }

 con = sqlite3.connect('prices.db')
 cur = con.cursor()

 cur.execute('''CREATE TABLE IF NOT EXISTS weekly_stats(
    name TEXT, price TEXT, date TEXT
 )''')

 insert = cur.execute(
    'INSERT INTO weekly_stats VALUES ("%s", "%s", "%s")' % (
       record['name'], record['price'], record['date']
       )
 )
 con.commit()
 con.close()


#Setting up webdriver
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path='./geckodriver', options=options)

#Getting data
driver.get("https://order.mandarake.co.jp/order/detailPage/item?itemCode=1158276027&ref=list&arrivalIndex=0")
price = driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
name = driver.find_element_by_xpath("//div[@class='subject']/h1").text
driver.close()

print(name)
print(price)
print(datetime.now().strftime('%-d %b %Y'))
save_data(name, price)