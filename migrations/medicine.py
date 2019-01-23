import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS medicine (id  int(10) PRIMARY KEY AUTO_INCREMENT,"
               "name char(50) ,price int(12),exp_date DATETIME)")
