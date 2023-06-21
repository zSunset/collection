'''Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, dzen-новости. 
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные новости в БД
Минимум один сайт, максимум - все три'''

from fake_useragent import UserAgent
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from lxml import html
from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()
LOGIN_MDB = os.getenv('LOGIN_MDB')
PASSWORD_MDB = os.getenv('PASSWORD_MDB')

uri = f"mongodb+srv://{LOGIN_MDB}:{PASSWORD_MDB}@cluster0.dqkosbc.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client['lesson_2']
mycol = mydb['collection']


user_agent = UserAgent().random
headers = {"User-Agent": user_agent,
        "Accept": "applications/json"}

response = requests.get('https://lenta.ru/', headers=headers)
dom = html.fromstring(response.text)
data = dom.xpath('//a[@class="card-mini _topnews"]')
data2 = dom.xpath('//a[@class="card-mini _longgrid"]')
all_data = data + data2
my_list = []

for i in data:
    dec = {}
    name_of_the_news = i.xpath('.//span[@class="card-mini__title"]/text()')
    link_to_news = i.xpath('./@href')
    publication_date = i.xpath(".//time[@class='card-mini__date']/text()")
    dec['наименование новости'] = name_of_the_news[0]
    dec['ссылку на новость'] = f'https://lenta.ru{link_to_news[0]}'
    dec['дата публикации'] = publication_date[0]
    my_list.append(dec)
mycol.insert_many(my_list)
