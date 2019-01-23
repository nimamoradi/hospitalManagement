import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS prescription (docter_id char(50) NOT NULL , id int(10) PRIMARY KEY NOT NULL , patient_id char(50) NOT NULL , `date` DATETIME);")
