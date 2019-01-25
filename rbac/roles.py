from request_management import db_mysql

roles = {
    "patient": "patient",
    "doctor": "doctor",
    "receptor": "receptor",
    "admin": "admin"

}


def role_lookup(role):
    if role in roles:
        return roles[role]
    else:
        return {'OK': False, 'Error': 'invalid role'}


def permission(role,role_arr):
    if role in role_arr:
        return True
    else:
        return False


def api_key_to_user(api_key):
    db = db_mysql.db_users['api_key']
    cursor = db_mysql.newCursor('api_key')

    cursor.execute(
        'SELECT users.* FROM users INNER JOIN api_keys ON '
        'users.username = api_keys.username WHERE api_keys.api_key =%s',
        (api_key,))
    db.commit()
    if cursor.rowcount == 0:
        return {'OK': False}

    return {'OK': True, "user": cursor.fetchone()}
