import hashlib
import secrets
import random
import smtplib
import string
import time
import datetime
from request_management import db_mysql, Mail


def edit_profile(j):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

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

    if password is not None and password != "":
        salt = secrets.token_hex(16)
        temp = (salt + password)
        hash = hashlib.sha512()
        hash.update(temp.encode('utf-8'))
        password = hash.hexdigest()
        cursor.execute("UPDATE `users` SET password = %s, salt = %s",
                       (password, salt,))
        db.commit()

    cursor.execute("UPDATE `users` SET name = %s, phone_number =%s, birth_year = %s, postal_code = %s, address = %s, weight = %s,\
                    gender = %s, height = %s",
                   (name, phone_number, birth_year, postal_code, address, weight, gender, height))
    db.commit()
    
    dict = {'OK': True}
    return dict


def login(j):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    username = j['username']
    password = j['password']
    if username is None or password is None:
        return {'OK': False, 'Error': "not a valid json"}

    cursor.execute(
        "SELECT  `username`, `name`, `phone_number`, `email`, `birth_year`, `postal_code`, `address`, `weight`, `gender`, `height`, `state`, `role` FROM users WHERE username = %s ;", (username,))
    db.commit()
    if cursor.rowcount <= 0:
        cursor.execute(
            "SELECT `username`, `name`, `phone_number`, `email`, `birth_year`, `postal_code`, `address`, `weight`, `gender`, `height`, `state`, `role` FROM users WHERE email = %s ;", (username,))
        db.commit()

    if cursor.rowcount <= 0:
        return {'OK': False, 'Error': "User doesn't exist"}

    row = cursor.fetchone()
    salt = row['salt']
    dbPassword = row['password']

    hash = hashlib.sha512()
    hash.update((salt + password).encode('utf-8'))
    enteredPassword = hash.hexdigest()
    # print("enteredPassword " + enteredPassword + "\n" + "has " + dbPassword)
    if dbPassword == enteredPassword:
        # T = int(time.time())
        Session = secrets.token_hex(16)
        cursor = db_mysql.newCursor()
        SessionExp = datetime.datetime.now() + datetime.timedelta(days=2)
        cursor.execute(
            "INSERT INTO api_keys (username, api_key, exp_date) VALUES (%s, %s, %s);",
            (username, Session, SessionExp))
        db.commit()
        return {'OK': True, 'api_key': Session, 'User': row}

    return {'OK': False, 'Error': "Wrong Password"}


def send_username_by_email(Email, Username):
    # design a user friendly email body

    # db = db_mysql.db
    # cursor = db_mysql.newCursor()
    # import datetime
    # expTime = datetime.datetime.now() + datetime.timedelta(days=1)
    # Token = secrets.token_hex(16)
    # cursor.execute(
    #     "INSERT INTO ActiviateTokens (Token, TokenExp, Username) VALUES (%s, %s, %s);",
    #     (Token, expTime, Username))
    # db.commit()

    body = "Your username is: \n%s" % (Username)
    Mail.mail(Email, "no-reply: Your hospital account username", body)


def checkLogin(session):
    t = datetime.datetime.now()
    cursor = db_mysql.newCursor()
    cursor.execute(
        "SELECT * FROM api_keys WHERE api_key = %s AND exp_date > %s ;", (session, t))
    if cursor.rowcount <= 0:
        return False

    row = cursor.fetchone()
    username = row['username']
    return username


def make_username(role):
    alphabet = string.ascii_lowercase
    db = db_mysql.db
    cursor = db_mysql.newCursor()
    while True:
        if role == "patient":
            username = ''.join(secrets.choice(alphabet) for i in range(4))
            username = "P%s" % username
            print("hello new username is %s" % username)
        # todo

        cursor.execute(
            'SELECT * FROM users WHERE username = %s ;', (username,))
        db.commit()

        if cursor.rowcount == 0:
            break

    return username
