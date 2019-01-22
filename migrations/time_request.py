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
    "CREATE TABLE IF NOT EXISTS time_request (id  int(10) PRIMARY KEY AUTO_INCREMENT, "
    "time_reserve_id  int(10) ,FOREIGN KEY (time_reserve_id) "
    "REFERENCES time_reserve(id),payed tinyint(1),"
    "patient_username char(50) ,FOREIGN KEY (patient_username) "
    "REFERENCES patient(username));")


