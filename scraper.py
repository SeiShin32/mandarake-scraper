from os import getloadavg
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from psql_con import psql_connection
import psycopg2, time



def get_driver():
    options = Options()
    options.add_argument('--headless')
    return webdriver.Firefox(executable_path='./geckodriver', options=options)

def get_links():
        con = psql_connection()
        cur = con.cursor()

        cur.execute('SELECT link_id, link from links')
        links = []
        link_id = 0
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

def scan_name(driver, link):
    driver.get(link)

    if 'mandarake' in link:
     try:
      name = driver.find_element_by_xpath("//div[@class='subject']/h1").text
      print(name + "\n" + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
      return name
     except TypeError:
      print("Couldn't scan mandarake page properly! Link: " + link)
     

    if 'suruga-ya' in link:
     try:
        name = driver.find_elements_by_xpath('//h1[@class="h1_title_product"]')[0].text
        print(name + "\n" + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
        return name
     except TypeError:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")
    

def scan_price(driver, link):
    driver.get(link)
    if 'mandarake' in link:
     try:
      price = driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
      print("\n" + price + "\n" + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
      return price                
     except TypeError:
      print("Couldn't scan mandarake page properly! Link: " + link)
     

    if 'suruga-ya' in link:
     try:
      price = driver.find_element_by_xpath("//span[@class='text-price-detail price-buy']").text
      price = ''.join(x for x in price if x.isdigit())
      print("\n" + price + "\n" + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
      return price
     except Exception:
      print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")
     
if __name__ == "__main__":
  driver = get_driver()
  links = get_links()

  for link in links:
        time.sleep(0.5)
        print(link[0])
        save_data(link[0], scan_price(driver, link[1]))
  driver.close()

 
     



