from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
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

mydb = client['New']
mycol = mydb['customers']


currency = int(input('Введите сумму минимальной зарплаты: '))
while currency:
    for i in mycol.find({'от': {'$gte': currency}}):
        print(i)