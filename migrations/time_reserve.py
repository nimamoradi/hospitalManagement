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
    "CREATE TABLE IF NOT EXISTS time_reserve (id  int(10)"
    " PRIMARY KEY AUTO_INCREMENT,hour int(4),week_day char(20),"
    " doctor_username char(50) ,FOREIGN KEY (doctor_username) "
    "REFERENCES doctor(username),"
    " price int(12));")
