import sqlite3, telebot, logging

bot = telebot.TeleBot("961483378:AAHVGshov7D5qC0ETdL0e5Q1OB8FtCGI5dA")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

def get_records():
 con = sqlite3.connect('prices.db', timeout = 10)
 cur = con.cursor()
 try:
  records = cur.execute('SELECT name, price, date FROM weekly_stats GROUP BY name ORDER BY MAX(date) DESC'
  ).fetchall()   
 except Exception:
    records = []
 con.close()
 records = ' '.join(str(e) for e in records)
 return records

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['text'])
def get_db_request(message):

	if message.text.lower() == 'db':	 
	 bot.reply_to(message, get_records())
	 
	if message.text.lower() == 'hoy':
	 bot.reply_to(message, "hoy!") 


bot.polling()