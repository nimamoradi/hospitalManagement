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
    "CREATE TABLE IF NOT EXISTS bed (id  int(10) PRIMARY KEY AUTO_INCREMENT, "
    "patient_username  char(50) ,FOREIGN KEY (patient_username) "
    "REFERENCES patient(username),payed tinyint(1) default 0,"
    "doctor_username char(50) ,FOREIGN KEY (doctor_username) "
    "REFERENCES doctor(username));")

