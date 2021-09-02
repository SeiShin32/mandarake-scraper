import sqlite3, telebot, logging

bot = telebot.TeleBot("961483378:AAHVGshov7D5qC0ETdL0e5Q1OB8FtCGI5dA")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

def get_data(query):
 con = sqlite3.connect('prices.db', timeout = 10)
 cur = con.cursor()
 try:
  records = cur.execute(query).fetchall()   
 except Exception:
  records = []
  print('Invalid query!')

 con.close()
 return records

def get_records():
 return ' '.join(str(e) for e in get_data('SELECT name, price, date FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'))

def get_titles():
 return ' '.join(str(e) for e in get_data('SELECT name FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'))

def get_titles_prices():
 return ' '.join(str(e) for e in get_data('SELECT name, price FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'))
	
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "SHO?")

@bot.message_handler(content_types=['text'])
def get_db_request(message):

	if message.text.lower() == 'hoy':
	 bot.reply_to(message, "Hoy!") 

	if message.text.lower() == 'get db':	 
	 bot.reply_to(message, get_records())

	if message.text.lower() == 'get titles':
	 bot.reply_to(message, get_titles()) 
	 
	if message.text.lower() == 'get titles with prices':
	 bot.reply_to(message, get_titles_prices()) 


bot.polling()