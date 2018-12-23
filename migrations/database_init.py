import mysql.connector
from config import database

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd']
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE " + database['db_name'])
