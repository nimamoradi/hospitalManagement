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
         },
        {"action": "SELECT, UPDATE, INSERT",
         "table": ["prescription"]
         },
        {"action": "SELECT",
         "table": ["prescription_item"]
         }
    ]
}

database_users['root'] = {
    "host": "localhost",
    "user": "root",
    "passwd": "",
    "db_name": "hospital"
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
        {"action": "SELECT, INSERT, UPDATE",
         "table": ["time_request", "users", "patient"]
         },
        {"action": "SELECT",
         "table": ["bed"]
         }
    ]
}
database_users['api_key'] = {
    "host": "localhost",
    "user": "api_key",
    "passwd": "ahgbskjdaui",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT",
         "table": ["users"]
         },
        {"action": "SELECT",
         "table": ["api_keys"]
         },
    ]
}
database_users['doctor'] = {
    "host": "localhost",
    "user": "doctor",
    "passwd": "asdtverver",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT",
         "table": ["medicine"]
         },
        {"action": "SELECT",
         "table": ["patient"]
         },
        {"action": "INSERT, UPDATE",
         "table": ["invoice_item"]
         },
        {"action": "SELECT, UPDATE, INSERT",
         "table": ["prescription"]
         },
        {"action": "SELECT, UPDATE, DELETE",
         "table": ["time_request"]
         },
        {"action": "SELECT, UPDATE, INSERT",
         "table": ["prescription_item"]
         },
        {"action": "SELECT, UPDATE, INSERT",
         "table": ["bed"]
         }
    ]
}

database_users['message'] = {
    "host": "localhost",
    "user": "message",
    "passwd": "dkskmvdsmvdl",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT, INSERT",
            "table": ["messages"]
         }
    ]
}

database_users['accounting'] = {
    "host": "localhost",
    "user": "accounting",
    "passwd": "dkskmvdsmvdl",
    "db_name": "hospital",
    "grants": [
        {"action": "SELECT, INSERT, UPDATE",
            "table": ["invoice_item"]
         }
    ]
}

# database_users['receptor'] = {
#     "host": "localhost",
#     "user": "root",
#     "passwd": "",
#     "db_name": "hospital",
#     "grants": [

#     ]
# }
