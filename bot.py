import telebot
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from sqlalchemy import create_engine, text

engine = create_engine('postgresql://assel:805671@localhost/assel')

conn = engine.connect()

bot = telebot.TeleBot("5099087754:AAHgiMdgExf9koLA3FAam-nNVybkvuGMLQo")


@bot.message_handler(commands=['start'])
def get_leetcode_username(message):
	bot.send_message(message.chat.id,
	'''Welcome to telegram leetcode rating bot!
	send me your leetcode username to keep track of your rating!''')

@bot.message_handler(commands=['get'], regexp = '\/get \w+')
def get_user_record(message):
	username = message.text[5:]
	chat_id = message.chat.id
	user_id = message.from_user.id
	easy, medium, hard = get_record(username)
	
	findUserRecord = text(
		'select * from record where chat_id = '+ str(chat_id) + ' and username = ' + "'" + username +"';"
	)

	x = conn.execute(findUserRecord).fetchall()
	print(x)

	if len(x) == 0:
		bot.send_message(chat_id, 'given username has not been set in this chat, try command /help to know more')
		return
	easy = x[0][2] - int(easy)
	medium = x[0][3] - int(medium)
	hard = x[0][4] - int(hard)

	bot.send_message(chat_id,  username + ': (easy - ' + str(easy) + ' medium - ' + str(medium) + ' hard - ' +  str(hard) +' total: ' + str(int(easy)+int(medium)+int(hard)) + ')')


@bot.message_handler(commands=['getFromStartDate'], regexp= '\/getFromStartDate \w+')
def from_start_date(message):
	username = message.text[18:]
	print(username)
	easy, medium, hard = get_record(username)

	bot.send_message(message.chat.id,  username + ': (easy - ' + str(easy) + ' medium - ' + str(medium) + ' hard - ' +  str(hard) +' total: ' + str(int(easy)+int(medium)+int(hard)) + ')')


	

def get_record(username):
	ser = Service('/app/drivers/chromedriver')

	browser = webdriver.Chrome(service=ser)

	url = 'https://www.leetcode.com/' + username
	browser.get(url)

	content = browser.page_source

	soup = BeautifulSoup(content, "html.parser")
	nums = []
	try:
		WebDriverWait(browser, 10).until(
			EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.difficulty-ac-count__jhZm'))
		)
	finally:
		nums = browser.find_elements(By.CSS_SELECTOR, 'span.difficulty-ac-count__jhZm')
		easyWrapper = nums[0]

		mediumWrapper = nums[1]
		hardWrapper = nums[2]	

	return easyWrapper.text, mediumWrapper.text, hardWrapper.text
	
@bot.message_handler(commands=['getOverallRating'])
def get_overall_rating(message):
	chat_id = message.chat.id
	getRatings = text(
		'select username, easies, mediums, hards from record where chat_id = ' + str(chat_id) +' order by easies+mediums+hards desc'
	)

	x = conn.execute(getRatings).fetchall()

	results = []

	for a in x:
		username = a[0]
		easy, medium, hard = get_record(username)
		print(easy, medium, hard)

		easy = int(a[1]) - int(easy)
		medium = int(a[2]) - int(medium)
		hard = int(a[3]) - int(hard)

		result = username + ': (easy - ' + str(easy) + ' medium - ' + str(medium) + ' hard - ' + str(hard) +' total: ' + str(easy+medium+hard) + ')'
		results.append(result)
		print(results)
	
	separator = ', \n'
	s = separator.join(results)
	bot.send_message(chat_id, s)

@bot.message_handler(commands=['getRating'])
def get_rating(message):
	chat_id = message.chat.id
	getRatings = text(
		'select username, easies, mediums, hards from record where chat_id = ' + str(chat_id) +' order by easies+mediums+hards desc'
	)
	x = conn.execute(getRatings).fetchall()

	results = []

	for a in x:
		username = a[0]
		easy, medium, hard = get_record(username)
		print(easy, medium, hard)

		easy = int(a[1])
		medium = int(a[2])
		hard = int(a[3])

		result = username + ': (easy - ' + str(easy) + ' medium - ' + str(medium) + ' hard - ' + str(hard) +')'
		results.append(result)
		print(results)
	
	separator = ', \n'
	s = separator.join(results)
	bot.send_message(chat_id, s)

@bot.message_handler(commands=['setLeetcodeUsername'], regexp = '\/setLeetcodeUsername \w+')
def send_welcome(message):
	username = message.text[21:]
	easy, medium, hard = get_record(username)
	user_id = message.from_user.id
	chat_id = message.chat.id
	print(easy)
	print(medium)
	print(hard)
	findUsernameOfUserInChar = text(
		'select * from record where chat_id = '+ str(chat_id) + ' and user_id = ' + "'" + str(user_id) +"'"
	)
	record = conn.execute(findUsernameOfUserInChar).fetchall()

	if len(record) == 0:
		insertIntoRecords = text('insert into record values ('+ str(chat_id) + ", " + str(user_id) +", " + str(easy) + ', ' + str(medium) + ', ' + str(hard) +",'" + username +"');" ) 
		conn.execute(insertIntoRecords)
	else:

		updateUsernameInRecord = text('update record set username = ' +"'" + username +"',  easies = " +str(easy) + ', mediums = '+ str(medium) +', hards = ' +str(hard) + ' where chat_id = ' +str(chat_id) + " and user_id = "  + str(user_id) +';')
		conn.execute(updateUsernameInRecord)

	bot.send_message(message.chat.id, 'your leetcode username has been set to ' + username)

bot.infinity_polling()