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

    reciever = j['reciever']
    message = j['message']
    api_key = j['api_key']

    if reciever is None or message is None or api_key is None:
        return {'OK': False, 'Error': "not a valid json"}

    username = check_login(api_key)

    cursor.execute("INSERT INTO messages(`sender`, `reciever`, `message`, `date`, `seen`)"
                   + " VALUES ( %s, %s, %s, CURRENT_TIMESTAMP, FALSE);",
                   (username, reciever, message,))
    db.commit()
   
    dict = {'OK': True}
    return dict


def get_messages(j):
    db = db_mysql.db_users['message']
    cursor = db_mysql.newCursor("message")

    api_key = j['api_key']

    if api_key is None:
        return {'OK': False, 'Error': "not a valid json"}

    username = check_login(api_key)

    cursor.execute("SELECT * FROM messages WHERE `reciever` = %s)",
                   (username))
    db.commit()

    dict = {'OK': True, "messages": cursor.fetchall()}
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
