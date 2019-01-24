import mysql.connector
from config import database, database_users

mydb = mysql.connector.connect(
    host=database['host'],
    user=database['user'],
    passwd=database['passwd'],
    database=database['db_name']
)

mycursor = mydb.cursor()

for key, row in database_users.items():
    mycursor.execute(
        "CREATE USER IF NOT EXISTS %s@localhost IDENTIFIED BY %s;", (row['user'], row['passwd']))
    mydb.commit()
    print("done creating user")
    for actions in row['grants']:
        for table in actions['table']:
            mycursor.execute(
                "GRANT %s ON hospital.%s TO %s@localhost;"% (actions['action'], table, row['user']))
            mydb.commit()


