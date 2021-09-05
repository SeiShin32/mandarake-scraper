from os import link
import sqlite3, telebot, logging, tele_token, get_stats

bot = telebot.TeleBot(tele_token.t_token)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

def insert_data(query):
 con = sqlite3.connect('prices.db', timeout = 10)
 cur = con.cursor()
 try:
  return cur.execute(query) 
 except Exception:
  print('Invalid query!')
  pass
 finally:
  con.commit()
  
def check_if_entry_exists(link):
  return insert_data("SELECT EXISTS(SELECT * FROM target_list WHERE link ='" + link + "');").fetchone()[0]

#Pulls data from the database

def get_data(query):
 con = sqlite3.connect('prices.db', timeout = 10)
 cur = con.cursor()
 try:
  records = cur.execute(query).fetchall()
  return records  
 except Exception:
  print('Invalid query!')
  pass
 finally:
  con.close()  

#Formats the data into a single, readable string; accepts SQL query as argument

def format_records(query):
 counter = 1
 final_string = ""
 for row in get_data(query):
  row = ' '.join(str(e) for e in row)
  final_string += str(counter) + '. ' + row + '\n'
  counter += 1
 return final_string
	
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hoy! Type 'help' if you want to see a list of available commands")

@bot.message_handler(commands=['help'])
def help(message):
	bot.reply_to(message, tele_token.msg)

@bot.message_handler(commands=['add'])
def add_link(message):
 link = message.text
 try:
  link = link.split(" ")[1]
 except IndexError:
  bot.reply_to(message, "There seems to be something wrong with the link (it's probably empty).")
  return None

 print("\n" + link + "\n")

 if check_if_entry_exists(link):
   bot.reply_to(message, "This link already exists!")
   return None
   
 insert_data('INSERT INTO target_list VALUES (NULL, "%s")' % (link))
 bot.reply_to(message, 'adding link')
  
@bot.message_handler(commands=['scan'])
def add_link(message):
  bot.reply_to(message, 'Scanning...')
  get_stats.scan()
  

@bot.message_handler(commands=['delete'])
def add_link(message):
    link = message.text
    try:
     link = link.split(" ")[1]
    except IndexError:
     bot.reply_to(message, "There seems to be something wrong with the link (it's probably empty).")
     return None

    if not check_if_entry_exists(link):
      bot.reply_to(message, "This link doesn't exist!")
      return None

    print("\n" + link + "\n")

    insert_data("DELETE FROM target_list WHERE link ='"+ link +"';")
    insert_data("DELETE FROM weekly_stats WHERE link ='"+ link +"';")
    bot.reply_to(message, 'deleting link')    	

@bot.message_handler(content_types=['text'])
def get_db_request(message):

	if message.text.lower() == 'hoy':
	 bot.reply_to(message, "Hoy!")

	if message.text.lower() == 'get db':	 
	 bot.reply_to(message, format_records('SELECT name, price, date FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'))

	if message.text.lower() == 'get titles':
	 bot.reply_to(message, format_records('SELECT name FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC')) 
	 
	if message.text.lower() == 'get titles with prices':
	 bot.reply_to(message, format_records('SELECT name, price FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'))

bot.polling()