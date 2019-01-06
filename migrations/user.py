import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute(
    "CREATE TABLE IF NOT EXISTS users (username  char(50) PRIMARY KEY,name VARCHAR(255), family_name VARCHAR(255),"
    "phone_number CHAR(15),"
    "password VARCHAR(150),salt VARCHAR(150),email VARCHAR(32),birth_date DATETIME,postal_code VARCHAR(32),"
    "address TEXT,weight TINYINT,gender TINYINT,height TINYINT,state TINYINT)")
