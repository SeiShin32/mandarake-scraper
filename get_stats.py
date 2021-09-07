from os import getloadavg
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from psql_con import psql_connection
import psycopg2, time


def get_links():
        sqliteConnection = psql_connection()
        cursor = sqliteConnection.cursor()

        sqlite_select_query = 'SELECT * from target_list'
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

        con = psql_connection()
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS price_stats(
     id serial PRIMARY KEY, name VARCHAR(255) NOT NULL, price VARCHAR(255) NOT NULL, link VARCHAR(255) NOT NULL, date VARCHAR(255) NOT NULL
     )''')

        con.commit()

        insert = cur.execute(
            "INSERT INTO price_stats(name, price, link, date) VALUES ('%s', '%s', '%s', '%s')" % (
                record['name'], record['price'], record['link'], record['date']
            )
        )

        con.commit()
        con.close()

# Setting up webdriver
options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(
    executable_path='./geckodriver', options=options)

# Getting data from every link

links = get_links()
for link in links: 
        driver.get(link)
        time.sleep(0.5)

        if 'mandarake' in link:
            try:
                price = driver.find_element_by_xpath(
                    "//meta[@itemprop='price']").get_attribute("content")
                name = driver.find_element_by_xpath(
                    "//div[@class='subject']/h1").text
                print(name + "\n" + price + "\n" +
                      datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
                save_data(name, price, link)
            except TypeError:
                print("Couldn't scan mandarake page properly! Link: " + link)

        if 'suruga-ya' in link:
            try:
                name = driver.find_elements_by_xpath(
                    '//h1[@class="h1_title_product"]')[0].text
                price = driver.find_element_by_xpath(
                    "//span[@class='text-price-detail price-buy']").text
                price = ''.join(x for x in price if x.isdigit())
                print(name + "\n" + price + "\n" +
                      datetime.now().strftime('%d/%m/%Y %H:%M') + "\n")
                save_data(name, price, link)
            except Exception:
                print("Couldn't scan suruga-ya page properly! Link: " + link + "\n")

driver.close()
