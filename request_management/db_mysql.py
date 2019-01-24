# -*- coding: utf-8 -*-
import MySQLdb
from migrations.config import database, database_users
# from ..migrations.config import database

print("Hi MySQL. I am legen wait for it...")
# Open database connection
db_users = {}
try:
    db = MySQLdb.connect(host=database['host'],
                         user=database['user'],
                         passwd=database['passwd'],
                         db=database['db_name'],
                         unix_socket="/opt/lampp/var/mysql/mysql.sock")
    db.set_character_set('utf8')

    for key, row in database_users.items():
        db_users[row['user']] = MySQLdb.connect(host=database_users[row['user']]['host'],
                                                user=database_users[row['user']]['user'],
                                                passwd=database_users[row['user']]['passwd'],
                                                db=database_users[row['user']]['db_name'],
                                                unix_socket="/opt/lampp/var/mysql/mysql.sock")
        db_users[row['user']].set_character_set('utf8')

except MySQLdb.Error as e:
    print(str(e))


def newCursor(db_user):
    crsr = db_users[db_user].cursor(MySQLdb.cursors.DictCursor)
    crsr.execute('SET NAMES utf8;')
    crsr.execute('SET CHARACTER SET utf8;')
    crsr.execute('SET character_set_connection=utf8;')
    return crsr


# prepare a cursor object using cursor() method
cursor = newCursor('login')
# execute SQL query using execute() method.
print("dary")
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print(str(data))
