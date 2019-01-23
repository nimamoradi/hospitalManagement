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
                'Error': 'no reserve with id found with doctor %s already exists in system ' % docter_username}
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
