import hashlib
import secrets
import random
import smtplib
import string
import time
import datetime

from rbac.roles import role_lookup
from request_management import db_mysql, Mail

from rbac.roles import roles


def register(j):
    db = db_mysql.db_users['signing']
    cursor = db_mysql.newCursor("signing")

    name = j['name']
    phone_number = j['phone_number']
    role = j['role']
    password = j['password']
    email = j['email']

    if phone_number is None or email is None or name is None or role is None:
        return {'OK': False, 'Error': "not a valid json"}

    salt = secrets.token_hex(16)
    temp = (salt + password)
    hash = hashlib.sha512()
    hash.update(temp.encode('utf-8'))
    password = hash.hexdigest()
    # Password = hashlib.sha512(temp).hexdigest()

    cursor.execute('SELECT * FROM users WHERE email = %s ;', (email,))
    print("     ")
    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount > 0:
        return {'OK': False, 'Error': 'Email %s already exists in system ' % cursor.fetchone()['email']}

    username = make_username(role)
    cursor.execute("INSERT INTO users(username, password, salt, email, name, phone_number, role)"
                   + " VALUES ( %s, %s, %s, %s, %s, %s, %s);",
                   (username, password, salt, email, name, phone_number, role,))
    if role == roles['doctor']:
        cursor.execute("INSERT INTO doctor (username) VALUES (%s);",
                       (username,))
    if role == roles['patient']:
        cursor.execute("INSERT INTO patient (username) VALUES (%s);",
                       (username,))
    if role == roles['receptor']:
        cursor.execute("INSERT INTO receptor (username) VALUES (%s);",
                       (username,))

    db.commit()
    try:
        send_username_by_email(email, username)
        pass
    except smtplib.SMTPRecipientsRefused as e:
        print("email not sent: Bad Recipient" + e)  # inform user
        ok = False
        error = "Email address not correct"

    dict = {'OK': True}
    return dict


def forget_password(j):
    db = db_mysql.db_users['signing']
    cursor = db_mysql.newCursor("signing")

    if 'email' in j:
        email = j['email']
    else:
        return {'OK': False, 'Error': "not a valid json"}

    cursor.execute('SELECT * FROM users WHERE email = %s ;', (email,))
    print("     ")
    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount == 0:
        return {'OK': False, 'Error': 'Email %s already exists in system ' % cursor.fetchone()['email']}

    new_password = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    salt = secrets.token_hex(16)
    temp = (salt + new_password)
    hash = hashlib.sha512()
    hash.update(temp.encode('utf-8'))
    password = hash.hexdigest()

    cursor.execute("UPDATE users SET"
                   " password = %s , salt = %s  WHERE email = %s",
                   (password, salt, email))
    db.commit()
    try:
        send_password_by_email(email, new_password)
        pass
    except smtplib.SMTPRecipientsRefused as e:
        print("email not sent: Bad Recipient" + e)  # inform user
        ok = False
        error = "Email address not correct"

    dict = {'OK': True}
    return dict




