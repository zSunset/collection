from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests


uri = "mongodb+srv://stavropolip:stavropolip@cluster0.dqkosbc.mongodb.net/"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client['New']
mycol = mydb['customers']


user_agent = UserAgent().random
headers = {"User-Agent": user_agent,
        "Accept": "applications/json"}
isHaveNextPage=True
page=1
while isHaveNextPage:
    response = requests.get(f'https://stavropol.hh.ru/search/vacancy?no_magic=true&L_save_area=true&resume=c4655aaaff0b260a710039ed1f577466656164&text=&excluded_text=&salary=&currency_code=RUR&only_with_salary=true&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&page={page}', headers=headers).text
    bs_soup = BeautifulSoup(response, 'lxml')
    data = bs_soup.find_all('div', class_='vacancy-serp-item-body__main-info')
    
    my_list = []
    if data != my_list:
        for datas in data:
            vacancy = datas.find('a', class_='serp-item__title')
            salary = datas.find('span', class_='bloko-header-section-3').text
            vacancys = vacancy.text
            vacancyc = vacancy.get('href')
            del_space = ''.join(salary.split())
            salarys = "".join([c if c.isdigit() else " " for c in del_space]).split()
            if salarys:
                my_from = int(salarys[0])
                try:
                    if salarys[1] == salarys:
                        before = int(salarys[1])
                except IndexError:
                    before = None
            currency = salary[-4:]
            dec = {'вакансия': vacancys, 'ссылка': vacancyc, 'от': my_from, 'до': before, 'валюта': currency}
            my_list.append(dec)

    mycol.insert_many(my_list)
    if bs_soup.find('a', class_='bloko-button') is None:
        isHaveNextPage=False
    page += 1
