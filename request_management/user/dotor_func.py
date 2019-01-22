from request_management import db_mysql


def search_doctor(docter_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('SELECT * FROM doctor WHERE username like %s ;', ('%' + docter_username + '%',))
    print((docter_username))
    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount == 0:
        return {'OK': False, 'Error': 'no doctor with id found %s already exists in system ' % docter_username}
    else:
        for row in cursor:
            print(row)
        dict = {'OK': True}
        dict['doctors'] = cursor.fetchall()
        return dict

    dict = {'OK': false}
    return dict
