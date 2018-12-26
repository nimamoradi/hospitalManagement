import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS prescriber (username char(50) ,FOREIGN KEY (username) REFERENCES users(username)   ON UPDATE CASCADE   ON DELETE RESTRICT)")