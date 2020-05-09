from bs4 import BeautifulSoup
from time import sleep
import urllib.request
import datetime
import telebot


# NEWS WEBSITES 

mal = 'https://myanimelist.net/news'
kgp = 'https://kg-portal.ru/news/anime/'
ann = 'https://animenewsnetwork.com/news'
cyr = 'https://crunchyroll.com/news'
okm = 'https://otakumode.com/news'
shm = 'https://shikimori.one/forum/news'


# BOT TOKEN AND ENABLING

tk = '971248982:AAE27YKh7BAIeRIikyE1qkIVHSTBAI23Oug'
bot = telebot.AsyncTeleBot(tk)


# USERS LIST AND USERS CLASS

users = {}

class User:
    def __init__(self, chatId):
        self.chatId = chatId
        self.mal = ""
        self.kgp = ""
        self.ann = ""
        self.cyr = ""
        self.okm = ""
        self.shm = ""


# GET SOUP FUNCTION

def get_soup(web):
    req = urllib.request.Request(web)
    resp = urllib.request.urlopen(req)
    Data = resp.read()
    return BeautifulSoup(Data, 'html.parser')


# PARSE MYANIMELIST

def parse_mal(index):

    soup = get_soup(mal)

    news = str(soup.find_all('p', {"class": "title"})[0].find('a').get('href'))
        
    if users[index].mal != news:
        print(news)
        users[index].mal = news
        bot.send_message(users[index].chatId, users[index].mal)
    
    
# PARSE KG PORTAL

def parse_kgp(index):

    soup = get_soup(kgp)

    news = "https://kg-portal.ru" + str(soup.find_all('a', {"class": "news_card_link"})[0].get('href'))

    if  users[index].kgp != news:
        print(news)
        users[index].kgp = news
        bot.send_message(users[index].chatId, users[index].kgp)
        

# PARSE ANIMENEWSNETWORK

def parse_ann(index):
    
    soup = get_soup(ann)
    
    news = "https://animenewsnetwork.com/" + str(soup.find_all('a')[9].get('href'))

    if  users[index].ann != news:
        print(news)
        users[index].ann = news
        bot.send_message(users[index].chatId, users[index].ann)
        

# PARSE CRUNCHYROLL

def parse_cyr(index):
    
    soup = get_soup(cyr)
    
    news = "https://crunchyroll.com" + str(soup.find_all('a')[17].get('href'))
    
    if  users[index].cyr != news:
        print(news)
        users[index].cyr = news
        bot.send_message(users[index].chatId, users[index].cyr)    


# PARSE OTAKUMODE

def parse_okm(index):

    soup = get_soup(okm)
    
    news = "https://otakumode.com" + str(soup.find_all('a', {"class": "inherit"})[5].get('href'))
    
    if  users[index].okm != news:
        print(news)
        users[index].okm = news
        bot.send_message(users[index].chatId, users[index].okm)
        

# PARSE SHIKMORI

def parse_shm(index):

    soup = get_soup(shm)

    news = str(soup.find_all('a', {"class": "name"})[0].get('href'))
        
    if users[index].shm != news:
        print(news)
        users[index].shm = news
        bot.send_message(users[index].chatId, users[index].shm)


# ROOT PARSING FUNCTION

def parsing(index):
    print("parsing " + str(datetime.datetime.now()))
    parse_mal(index)
    parse_kgp(index)
    parse_ann(index)
    parse_cyr(index)
    parse_okm(index)
    parse_shm(index)


# START BOT HANDLER AND LOOP FUNCTION

@bot.message_handler(commands=['start'])
def startBot(message):

    temp = User(message.from_user.id)
    
    if temp not in users:
        users[message.from_user.id] = temp
        bot.send_message(temp.chatId, "Starting... Wait for the news to come!")
        
    while(True):
        parsing(message.from_user.id)
        sleep(300)


bot.infinity_polling()
