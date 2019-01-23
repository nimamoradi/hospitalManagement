roles = {
    "patient": "patient",
    "doctor": "doctor",
    "receptor": "receptor"

}


def role_lookup(role):
    if role in roles:
        return roles[role]
    else:
        return {'OK': False, 'Error': 'invalid role'}
