import request_management
from request_management import db_mysql, Mail
import request_management.user.receptor


def search_doctor(docter_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    cursor.execute('SELECT * FROM doctor WHERE username like %s ;',
                   ('%' + docter_username + '%',))
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
        '(time_reserve.id = time_request.time_reserve_id) WHERE time_reserve.id = %s AND time_reserve.doctor_username = %s'
        ' AND time_request.time_reserve_id IS NOT NULL;',
        (reserve_id, doctor_username))
    user = cursor.fetchone()
    print(user)
    db.commit()
    send_email(user['email'], user['name'] +
               ", your reservation is cancelled by doctor " + doctor_username)
    request_management.user.receptor.cancel_reserve(reserve_id)
    return {'OK': True}


def accept_reserve(reserve_id, doctor_username):
    db = db_mysql.db
    cursor = db_mysql.newCursor()
    cursor.execute(
        'SELECT users.* FROM (patient LEFT OUTER JOIN users ON '
        '(patient.username = users.username) ),'
        'time_reserve LEFT OUTER JOIN time_request ON '
        '(time_reserve.id = time_request.time_reserve_id) WHERE time_reserve.id = %s '
        'AND time_reserve.doctor_username = %s'
        ' AND time_request.time_reserve_id IS NOT NULL;',
        (reserve_id, doctor_username))
    user = cursor.fetchone()
    print(user)
    db.commit()
    cursor.execute(
        'UPDATE time_request set active=1 WHERE time_reserve_id= %s', (reserve_id,))
    db.commit()
    cursor.execute(
        "INSERT INTO `invoice_item`(`name`, `unit`, `origin`, `patient`, `type`, `unit_price`, `date`, `paid`) VALUES\
        (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, FALSE)", "reservation", 1, doctor_username, user['username'], "reservation", 45000,)
    send_email(user['email'], user['name'] +
               ", your reservation is accepted by doctor " + doctor_username)

    

    return {'OK': True}


def prescribe(patient_username, doctor_username, items):
    db = db_mysql.db

    cursor = db_mysql.newCursor()
    cursor2 = db_mysql.newCursor()
    cursor.execute(
        'INSERT INTO prescription (docter_id,patient_id,date) VALUES (%s,%s,CURRENT_TIMESTAMP);',
        (doctor_username, patient_username,))
    prescription = cursor.lastrowid
    print(prescription)
    db.commit()
    for item in items:
        if item["typelord"] == "d":
            cursor.execute(
                'INSERT INTO labratory (`doctor`, `patient`, `type`, `result`, `paid`, `description`) VALUES (%s,%s,%s,%s,%s,%s);',
                (prescription, item['id'], item['type'], "", False, item['desc']))
        else:    
            cursor.execute(
                'INSERT INTO prescription_item (prescription_id,medicine_id, dose) VALUES (%s,%s,%s);',
                (prescription, item['id'], item['dose']))
        cursor2.execute("SELECT price FROM medicine WHERE medicine_id = %s", item['id'])
        price = cursor2.fetchone()['price']
        cursor.execute(
            "INSERT INTO `invoice_item`(`name`, `unit`, `origin`, `patient`, `type`, `unit_price`, `date`, `paid`) VALUES\
            (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, FALSE)", item['id'], item['dose'], doctor_username, patient_username, "prescription", price,)
    db.commit()

    return {'OK': True}


def prescribe(patient_username):
    db = db_mysql.db

    cursor = db_mysql.newCursor()
    cursor2 = db_mysql.newCursor()

    cursor2.execute(
        "SELECT * FROM labratory WHERE paid = TRUE AND patient =  %s and result IS NOT NULL", patient_username)
    db.commit()

    return {'OK': True, results= cursor.fetchall()}


def get_medicine_history(patient_username):
    db = db_mysql.db_users['doctor']
    cursor = db_mysql.newCursor('doctor')
    cursor.execute(
        'SELECT patient_id, medicine.Name ,unix_timestamp(prescription.date) FROM prescription_item INNER JOIN prescription ON prescription.id = prescription_item.prescription_id INNER JOIN medicine ON medicine.id = prescription_item.medicine_id WHERE prescription.patient_id = %s',
        (patient_username,))
    user = cursor.fetchall()
    print(user)
    db.commit()
    return {'OK': True, 'prescription': user}


def send_email(Email, body):
    Mail.mail(Email, "no-reply: Your hospital account reservations", body)


def hospitalize(patient_username, doctor_username):
    db = db_mysql.db_users['doctor']
    cursor = db_mysql.newCursor('doctor')
    cursor.execute(
        'INSERT INTO bed(patient_username,doctor_username)'
        'VALUES (%s,%s)',
        (patient_username, doctor_username))
    user = cursor.fetchall()
    print(user)
    db.commit()
    return {'OK': True}
