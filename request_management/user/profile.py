import hashlib
import secrets
import random
import smtplib
import string
import time
import datetime
from request_management import db_mysql, Mail


def edit_profile(j):
    db = db_mysql.db_users['patient']
    cursor = db_mysql.newCursor("patient")

    api_key = j['api_key']
    name = j['name']
    phone_number = j['phone_number']
    birth_year = j['birth_year']
    postal_code = j['postal_code']
    address = j['address']
    weight = j['weight']
    gender = j['gender']
    height = j['height']
    password = j['password']

    if api_key is None:
        return {'OK': False, 'Error': "You are not logged in"}
    username = check_login(api_key)
    if username is False:
        return {'OK': False}
    if password is not None and password != "":
        salt = secrets.token_hex(16)
        temp = (salt + password)
        hash = hashlib.sha512()
        hash.update(temp.encode('utf-8'))
        password = hash.hexdigest()
        cursor.execute("UPDATE `users` SET password = %s, salt = %s WHERE username = %s",
                       (password, salt, username,))
        db.commit()

    cursor.execute("UPDATE `users` SET name = %s, phone_number =%s, birth_year = %s, postal_code = %s, address = %s, weight = %s,\
                    gender = %s, height = %s WHERE username = %s",
                   (name, phone_number, birth_year, postal_code, address, weight, gender, height, username,))
    db.commit()

    dict = {'OK': True}
    return dict


def check_login(session):
    t = datetime.datetime.now()
    cursor = db_mysql.newCursor()
    cursor.execute(
        "SELECT * FROM api_keys WHERE api_key = %s AND exp_date > %s ;", (session, t))
    if cursor.rowcount <= 0:
        return False

    row = cursor.fetchone()
    username = row['username']
    return username
