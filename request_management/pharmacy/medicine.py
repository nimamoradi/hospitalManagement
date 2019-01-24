from datetime import datetime, date
from json import dumps

from request_management import db_mysql, Mail

import json


def search_medicine(medicine_name):
    db = db_mysql.db_users['pharmacy']
    cursor = db_mysql.newCursor("pharmacy")

    cursor.execute('SELECT `id`, `name`, `price`, unix_timestamp(exp_date) FROM medicine WHERE name like %s ;',
                   ('%' + medicine_name + '%',))
    print(medicine_name)
    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount == 0:
        return {'OK': False, 'Error': 'no medicine with the name %s found' % medicine_name}
    else:
        for row in cursor:
            print(row)
        return {'OK': True, 'medicines': cursor.fetchall()}


def add_medicine(name, price, exp_date):
    db = db_mysql.db_users['pharmacy']
    cursor = db_mysql.newCursor("pharmacy")

    cursor.execute(
        'INSERT INTO medicine(name,price,exp_date) values (%s,%s,%s);', (name, price, exp_date))
    db.commit()
    return {'OK': True, }


def get_medicine(id):
    db = db_mysql.db_users['pharmacy']
    cursor = db_mysql.newCursor("pharmacy")

    cursor.execute(
        'SELECT `id`, `name`, `price`, unix_timestamp(exp_date) FROM medicine WHERE id = %s ;', (id,))
    db.commit()
    return {'OK': True, 'medicine': cursor.fetchall()}


def get_prescription_details(items):
    db = db_mysql.db_users['pharmacy']
    cursor = db_mysql.newCursor("pharmacy")

    sql = "select `id`, `name`, `price`, unix_timestamp(exp_date) from medicine where id in (%s)" % (', '.join(str(id) for id in items))

    cursor.execute(sql)
    db.commit()
    return {'OK': True, 'prescription': cursor.fetchall()}


def update_medicine(id, price, exp_date):
    db = db_mysql.db_users['pharmacy']
    cursor = db_mysql.newCursor("pharmacy")

    cursor.execute(
        'UPDATE medicine SET price = %s , exp_date =%s WHERE id =%s;', (price, exp_date, id))
    db.commit()
    return {'OK': True, 'medicine': cursor.fetchall()}


def get_medicine_bydate():
    db = db_mysql.db_users['pharmacy']
    cursor = db_mysql.newCursor("pharmacy")

    cursor.execute(
        'SELECT `id`, `name`, `price`, unix_timestamp(exp_date) FROM medicine order by exp_date;', ())
    db.commit()
    return {'OK': True, 'medicines': cursor.fetchall()}

# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""

#     if isinstance(obj, datetime):
#         return obj.isoformat()
#     return obj
