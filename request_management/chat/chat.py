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


def send_message(j):
    db = db_mysql.db_users['message']
    cursor = db_mysql.newCursor("message")

    destination = j['destination']
    message = j['message']
    api_key = j['api_key']

    if destination is None or message is None or api_key is None:
        return {'OK': False, 'Error': "not a valid json"}

    username = check_login(api_key)

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
