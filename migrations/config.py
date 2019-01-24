database = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "db_name": "hospital"
}

database_users = {}

database_users['signing'] = {
    "host": "localhost",
    "user": "signing",
    "passwd": "sLdFnBlOvBkBnGkUdKUlf",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT, UPDATE, INSERT",
            "table": ["users", "patient", "doctor", "receptor", "api_keys"]
        }
    ]
}

# database_users['doctor'] = {
#     "host": "localhost",
#     "user": "root",
#     "passwd": "",
#     "db_name": "hospital",
#     "grants": [

#     ]
# }

# database_users['patient'] = {
#     "host": "localhost",
#     "user": "root",
#     "passwd": "",
#     "db_name": "hospital"
#     "grants": [

#     ]
# }

# database_users['receptor'] = {
#     "host": "localhost",
#     "user": "root",
#     "passwd": "",
#     "db_name": "hospital",
#     "grants": [

#     ]
# }
