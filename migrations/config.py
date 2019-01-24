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

database_users['pharmacy'] = {
    "host": "localhost",
    "user": "pharmacy",
    "passwd": "fckvndmvdovdlv",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT, UPDATE, INSERT",
            "table": ["medicine"]
        },
        {"action": "INSERT, UPDATE",
         "table": ["invoice_item"]
        }
    ]
}

database_users['patient'] = {
    "host": "localhost",
    "user": "patient",
    "passwd": "dkskmvmvdl",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT",
            "table": ["time_reserve"]
        },
        {"action": "SELECT, INSERT",
         "table": ["time_request"]
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

# database_users['receptor'] = {
#     "host": "localhost",
#     "user": "root",
#     "passwd": "",
#     "db_name": "hospital",
#     "grants": [

#     ]
# }
