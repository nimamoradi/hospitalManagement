import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS prescription (docter_id char(50) NOT NULL ,prescribed TINYINT(1),"
                 "id int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT , "
                 "patient_id char(50) NOT NULL , `date` DATETIME,FOREIGN KEY (docter_id) "
                 "REFERENCES doctor(username),FOREIGN KEY (patient_id) "
                 "REFERENCES patient(username));")
