import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

cursor = mydb.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS prescription_item (prescription_id int(10) NOT NULL ,"
               " id int(10) PRIMARY KEY NOT NULL AUTO_INCREMENT, medicine_id int(10) NOT NULL , "
               "dose char(50),FOREIGN KEY (medicine_id) "
               "REFERENCES medicine(id),"
               "FOREIGN KEY (prescription_id) "
               "REFERENCES prescription(id));")
