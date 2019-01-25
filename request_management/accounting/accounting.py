import hashlib
import secrets
import random
import smtplib
import string
import time
import datetime
import request_management.user.profile as profile
from rbac.roles import role_lookup
from request_management import db_mysql, Mail

from rbac.roles import roles


def get_invoice(j):
    db = db_mysql.db_users['accounting']
    cursor = db_mysql.newCursor("accounting")

    patient_name = j['patient_username']
    api_key = j['api_key']

    username = profile.check_login(api_key)

    cursor.execute("SELECT FROM invoice_item WHERE patient = %s", (patient_name, ))
    db.commit()
    
    dict = {'OK': True, 'invoice_items': cursor.fetchall()}
    return dict


def pay(j):
    db = db_mysql.db_users['accounting']
    cursor = db_mysql.newCursor("accounting")

    api_key = j['api_key']
    items = j['items']
    username = profile.check_login(api_key)

    for id in items:
        cursor.execute("UPDATE invoice_item SET pain = True WHERE id = %s", (id,))
        db.commit()

    dict = {'OK': True, 'invoice_items': cursor.fetchall()}
    return dict
