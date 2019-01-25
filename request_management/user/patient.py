import request_management
from request_management import db_mysql, Mail
import request_management.user.receptor


def see_bed(patient_username):
    db = db_mysql.db_users['doctor']
    cursor = db_mysql.newCursor('doctor')
    cursor.execute(
        'SELECT FROM bed WHERE patient_username = %s;',
        (patient_username,))
    user = cursor.fetchall()
    print(user)
    db.commit()
    return {'OK': True, 'beds': user}
