import hashlib
import secrets

import mysql.connector

from migrations.config import database


def seed(password):
    mydb = mysql.connector.connect(
        host=database['host'],
        user=database['user'],
        passwd=database['passwd'],
        database=database['db_name']
    )

    cursor = mydb.cursor()
    salt = secrets.token_hex(16)
    temp = (salt + password)
    hash = hashlib.sha512()
    hash.update(temp.encode('utf-8'))
    password = hash.hexdigest()
    cursor.execute("INSERT IGNORE INTO users(username, password, salt, email, name, phone_number, role)"
                   + " VALUES ( 'admin', %s, %s, 'admin', 'admin', 0, 'admin');",
                   (password, salt))

    cursor.execute("INSERT IGNORE INTO admin (username) VALUES ('admin');")
    mydb.commit()
