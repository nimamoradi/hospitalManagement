from request_management import db_mysql


def see_doctor_times(docter_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute(
        'SELECT  time_reserve.* FROM time_reserve LEFT OUTER JOIN time_request ON (time_reserve.id = time_request.time_reserve_id) WHERE time_reserve.doctor_username = %s AND time_request.time_reserve_id IS NULL;',
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



def reserve_doctor_time(reserve_id, patient_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute(
        'SELECT  time_reserve.* FROM time_reserve LEFT OUTER JOIN time_request ON (time_reserve.id = time_request.time_reserve_id) '
        ' WHERE time_reserve.id = %s AND time_request.time_reserve_id IS NULL;',
        (reserve_id, ))

    print(cursor.rowcount)

    if cursor.rowcount == 0:
        return {'OK': False, 'Error': 'no reserve with id found id %s already exists in system ' % reserve_id}
    else:
        time_reserve = cursor.fetchone()
        print(time_reserve)
        cursor.execute(
            "INSERT INTO time_request(time_reserve_id, payed, patient_username) VALUES (%s, %s, %s);",
            (time_reserve['id'], 0, patient_username))
        db.commit()
        dict = {'OK': True}
        return dict
