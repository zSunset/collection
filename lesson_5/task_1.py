'''Написать программу, которая собирает товары «Самые просматриваемые» с сайта техники mvideo и складывает данные в БД. 
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары'''

from fake_useragent import UserAgent
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from collections import ChainMap
import time
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

mydb = client['lesson_5']
mycol = mydb['collection']

random_user_agent = UserAgent().random

options = webdriver.ChromeOptions()
options.add_argument(f'{random_user_agent}')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)



url = 'https://www.mvideo.ru/'
service = Service(executable_path='/home/sunset/Рабочий стол/collection/lesson_5/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
my_list = []
my_list_2 = []
driver.get(url=url)
time.sleep(5)
driver.execute_script("window.scrollBy(0,1000)" , "")
time.sleep(10)
name = driver.find_elements(By.XPATH, '//div[@_ngcontent-serverapp-c156][@class="title"]')

for i in name:
    dec = {}
    dec['наименование товара'] = i.text
    dec['ссылка на товар'] = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
    my_list.append(dec)

price = driver.find_elements(By.XPATH, '//mvid-price[@_ngcontent-serverapp-c156][@class="price ng-star-inserted"]')

for t in price:
    zec = {}
    zec['цена со скидкой и без'] = t.text
    my_list_2.append(zec)



mycol.insert_many(my_list)