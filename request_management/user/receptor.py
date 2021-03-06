from request_management import db_mysql


def see_doctor_times(docter_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute(
        'SELECT time_reserve.*,(select time_request.time_reserve_id IS NOT NULL) as reserved FROM time_reserve LEFT OUTER JOIN time_request ON (time_reserve.id = time_request.time_reserve_id) WHERE time_reserve.doctor_username = %s ;',
        (docter_username,))

    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount == 0:
        return {'OK': False,
                'Error': 'doctor %s not found' % docter_username}
    else:
        for row in cursor:
            print(row)
        dict = {'OK': True}
        dict['reserve'] = cursor.fetchall()
        return dict


def cancel_reserve(reserve_id):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute(
        'DELETE FROM time_request WHERE time_reserve_id = %s;',
        (reserve_id,))

    print(cursor.rowcount)
    db.commit()
    return {'OK': True}


def add_doctor_time(doctor_username, week_day, hour,price):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute(
        'INSERT INTO time_reserve (doctor_username,week_day,hour,price)'
        'VALUES (%s,%s,%s, %s);',
        (doctor_username, week_day, hour,price))

    print(cursor.rowcount)
    db.commit()
    return {'OK': True}


def delete_doctor_time(id):
    db = db_mysql.db
    cursor = db_mysql.newCursor()
    cursor.execute(
        'DELETE time_request FROM time_request INNER JOIN time_reserve ON time_reserve.id='
        'time_request.time_reserve_id WHERE time_reserve_id = %s;',
        (id,))
    cursor.execute(
        'DELETE  time_reserve FROM time_reserve WHERE id = %s;',
        (id,))
    print(cursor.rowcount)
    db.commit()
    return {'OK': True}
