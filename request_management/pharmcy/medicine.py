from datetime import datetime, date
from json import dumps

from request_management import db_mysql, Mail

import json


def search_medicine(medicine_name):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('SELECT * FROM medicine WHERE name like %s ;', ('%' + medicine_name + '%',))
    print(medicine_name)
    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount == 0:
        return {'OK': False, 'Error': 'no medicine with name found %s already exists in system ' % medicine_name}
    else:
        for row in cursor:
            print(row)
        return {'OK': True, 'medicines': dumps(cursor.fetchall(), default=json_serial)}


def add_medicine(name, price, exp_date):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('INSERT INTO medicine(name,price,exp_date) values (%s,%s,%s);', (name, price, exp_date))
    db.commit()
    return {'OK': True, }


def get_medicine(id):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('SELECT * FROM medicine WHERE id = %s ;', (id,))
    db.commit()
    return {'OK': True, 'medicine': dumps(cursor.fetchone(), default=json_serial)}


def update_medicine(id, price, exp_date):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('UPDATE medicine SET price = %s , exp_date =%s WHERE id =%s;', (price, exp_date, id))
    db.commit()
    return {'OK': True, 'medicine': json.dumps(cursor.fetchone(), default=json_serial)}


def get_medicine_bydate():
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('SELECT * FROM medicine order by exp_date;', ())
    db.commit()
    return {'OK': True, 'medicines':  dumps(cursor.fetchall(), default=json_serial)}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
