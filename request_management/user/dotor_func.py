import request_management
from request_management import db_mysql, Mail
import request_management.user.receptor


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

        return {'OK': True, 'doctors': cursor.fetchall()}


def cancel_reserve(reserve_id, doctor_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()
    cursor.execute(
        'SELECT  users.* FROM (patient LEFT OUTER JOIN users ON '
        '(patient.username = users.username) ),'
        'time_reserve LEFT OUTER JOIN time_request ON '
        '(time_reserve.id = time_request.time_reserve_id) WHERE time_reserve.id = %s'
        ' AND time_request.time_reserve_id IS NOT NULL;',
        (reserve_id,))
    user = cursor.fetchone()
    print(user)
    db.commit()
    send_email(user['email'], user['name'] + ", your reservation is cancelled by doctor ")
    request_management.user.receptor.cancel_reserve(reserve_id)
    return {'OK': True}


def send_email(Email, body):
    Mail.mail(Email, "no-reply: Your hospital account reservations", body)
