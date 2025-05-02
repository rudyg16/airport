import pymysql
from dotenv import load_dotenv
import os
#load .env file
load_dotenv()
#Access env variables
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

connection = pymysql.connect(
    host = host,
    user = user,
    password=password,
    database= db_name,
    cursorclass=pymysql.cursors.DictCursor
)
with connection.cursor() as cursor:


airlines = ["American Airlines","Delta","United Airlines","Southwest Airlines","JetBlue"] 