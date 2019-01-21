import hashlib
import secrets
import random
import smtplib
import string
import time
import datetime
from request_management import db_mysql, Mail

def register(j):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    name = j['name']
    phone_number = j['phone_number']
    role = j['role']
    password = j['password']
    email = j['email']

    if phone_number is None or email is None or name is None or role is None:
         return {'OK': False, 'Error': "not a valid json"}

    salt = secrets.token_hex(16)
    temp = (salt + password)
    hash = hashlib.sha512()
    hash.update(temp.encode('utf-8'))
    password = hash.hexdigest()
    # Password = hashlib.sha512(temp).hexdigest()


    cursor.execute('SELECT * FROM users WHERE email = %s ;', (email,))
    print("     ")
    print(cursor.rowcount)
    db.commit()
    if cursor.rowcount > 0:
        return {'OK': False, 'Error': 'Email %s already exists in system ' % cursor.fetchone()['email']}
    
    username = make_username(role)
    cursor.execute("INSERT INTO users(username, password, salt, email, name, phone_number, role)"
                   + " VALUES ( %s, %s, %s, %s, %s, %s, %s);",
                   (username, password, salt, email, name, phone_number, role, ))
    db.commit()
    try:
        # send_username_by_email(email, username)
        pass
    except smtplib.SMTPRecipientsRefused as e:
        print("email not sent: Bad Recipient" + e)  # inform user
        ok = False
        error = "Email address not correct"

    dict = {'OK': True}
    return dict


def login(j):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    username = j['username']
    password = j['password']
    if username is None or password is None:
        return {'OK': False, 'Error': "not a valid json"}

    cursor.execute(
        "SELECT * FROM users WHERE username = %s ;", (username,))
    db.commit()
    if cursor.rowcount <= 0:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s ;", (username,))
        db.commit()

    if cursor.rowcount <= 0:
        return {'OK': False, 'Error': "User doesn't exist"}

    row = cursor.fetchone()
    salt = row['salt']
    dbPassword = row['password']

    hash = hashlib.sha512()
    hash.update((salt + password).encode('utf-8'))
    enteredPassword = hash.hexdigest()
    # print("enteredPassword " + enteredPassword + "\n" + "has " + dbPassword)
    if dbPassword == enteredPassword:
        # T = int(time.time())
        Session = secrets.token_hex(16)
        cursor = db_mysql.newCursor()
        SessionExp = datetime.datetime.now() + datetime.timedelta(days=2)
        cursor.execute(
            "INSERT INTO api_keys (username, api_key, exp_date) VALUES (%s, %s, %s);",
            (username, Session, SessionExp))
        db.commit()
        return {'OK': True, 'api_key': Session, 'User': row}
        
    return {'OK': False, 'Error': "Wrong Password"}


def send_username_by_email(Email, Username):
    # design a user friendly email body

    # db = db_mysql.db
    # cursor = db_mysql.newCursor()
    # import datetime
    # expTime = datetime.datetime.now() + datetime.timedelta(days=1)
    # Token = secrets.token_hex(16)
    # cursor.execute(
    #     "INSERT INTO ActiviateTokens (Token, TokenExp, Username) VALUES (%s, %s, %s);",
    #     (Token, expTime, Username))
    # db.commit()

    body = "your username is: \n %s" % (Username)
    Mail.mail(Email, "no-reply: Your hospital account username", body)


def checkLogin(session):
    t = datetime.datetime.now()
    cursor = db_mysql.newCursor()
    cursor.execute(
        "SELECT * FROM api_keys WHERE api_key = %s AND exp_date > %s ;", (session, t))
    if cursor.rowcount <= 0:
        return False

    row = cursor.fetchone()
    Username = row['username']
    return Username

def make_username(role):
    alphabet = string.ascii_lowercase
    db = db_mysql.db
    cursor = db_mysql.newCursor()
    while True:
        if role == "patient":
            username = ''.join(secrets.choice(alphabet) for i in range(4))
            username = "P%s" % username
            print("hello new username is %s" % username )
        # todo 


        cursor.execute(
            'SELECT * FROM users WHERE username = %s ;', (username,))
        db.commit()

        if cursor.rowcount == 0:
            break

    return username
    
