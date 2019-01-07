# -*- coding: utf-8 -*-
import binascii
import codecs
import datetime
import hashlib
import secrets

import time
import os
import random
import smtplib
import string
from bottle import Bottle, get, post, route, run, template, request, hook, response

# import cronJobs
# import botManager
from reqest_mangment import db_mysql, Mail

print("hi server")

serverAddrs = "http://localhost:2228"


@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@route('/')
def index():
    return 'goto <a href="./hello/mamad">hello page</a>'


indx = 0


@get('/ip')  # route == get1
def index():
    print("hello from ip")
    ip = request.environ.get('REMOTE_ADDR')

    return template("Your IP = {{ip}}", ip=ip)


# # کرون جاب های برنامه (اکسپایر کردن توکن ها) باید حداقل هر دقیقه صدا زده شود
# @get('/cronJob')  # route == get1
# def index():
#     cronJobs.deleteOldSessions()
#     return {'OK': True}

# تایید کردن اکانت توسط لینکی که ایمیل شده
@get('/confirm')
def index():
    dict = confirmEmail()
    return dict


@route('/login', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = login(j)
    return dict  # send api result as json, no need to encode


@route('/register', method=['POST', 'OPTIONS'])
def index():
    # TODO XSS safe the input
    print("request" + str(request))
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = register(j)
    return dict  # send api result as json, no need to encode


@route('/json', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json
    print("hello from json")

    # botManager.set_account_setting("mghayour7362",j)

    log = {'Name': 'Zara', 'title': "pro", 'Class': 'First'}
    return log  # a # send api result as json, no need to encode


@post('/json2/<user>')  # also we can get url parameters
def index(user):
    j = request.json
    a = {'a': 0, 'b': 1}
    a['title'] = j['title']
    a['user'] = user  # use url parameters like this
    return a


@route('/uploadPhoto', method=['POST', 'OPTIONS'])
def do_upload():
    account_name = request.forms.get('account_name')
    session = request.forms.get('Session')
    time_stamp = request.forms.get('TimeStamp')
    caption = request.forms.get('Caption')

    # check for login and account owner ship
    Username = checkLogin(session)
    if Username == False:
        return {'OK': False, 'Error': "You are not logged in"}

    if not check_account_ownership(Username, account_name):
        return {'OK': False, 'Error': "Not your Account"}

    try:
        upload = request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.jpg'):
            return "File extension not allowed."
        # check if folder exists
        if not os.path.exists("./Photos"):
            os.makedirs("./Photos")
        # generate a random string for files with same name
        rand = ''.join([random.choice(string.ascii_letters + string.digits)
                        for n in range(10)])
        file_path = "Photos/{file}".format(file=Username +
                                                "-" + rand + upload.filename)
        upload.save(file_path)

        cursor = db_mysql.newCursor()
        cursor.execute(
            "INSERT INTO 'Photos'('Username', 'PhotoName', 'PhotoCaption', 'PostTime') VALUES (%s, %s, %s, %s)",
            (Username, file_path, caption, time_stamp))

    except Exception as e:
        return "somthing went wrong"

    return "File successfully saved "


def confirmEmail():
    Token = str(request.GET.get('token', '').strip())
    db = db_mysql.db
    cursor = db_mysql.newCursor()
    cursor.execute(
        "SELECT * FROM ActiviateTokens WHERE Token = %s;", (Token,))
    if cursor.rowcount <= 0:
        return {'OK': False, 'Error': 'Incorrect Token'}

    row = cursor.fetchone()
    Username = row['Username']
    TokenExp = row['TokenExp']
    import datetime
    if TokenExp < datetime.datetime.now():
        return {'OK': False, 'Error': 'Expired Token'}

    cursor = db_mysql.newCursor()
    cursor.execute(
        "UPDATE Users SET state = True WHERE Username = %s", (Username,))
    cursor.execute(
        "DELETE FROM ActiviateTokens WHERE Username = %s", (Username,))
    db.commit()

    dict = {'OK': True}
    return dict


def register(j):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    Username = j['Username']
    FirstName = j['FirstName']
    LastName = j['LastName']
    Password = j['Password']
    Email = j['Email']

    # if CellNumber is None or Email is None or Password in None or LastName is None or FirstName is None or Username is None:
    #     return {'OK': False, 'Error': "not a valid json"}

    Salt = secrets.token_hex(16)
    temp = (Salt + Password)
    hash = hashlib.sha512()
    hash.update(temp.encode('utf-8'))
    Password = hash.hexdigest()
    # Password = hashlib.sha512(temp).hexdigest()

    cursor.execute(
        'SELECT * FROM users WHERE username = %s ;', (Username,))
    if cursor.rowcount > 0:
        return {'OK': False, 'Error': 'Username already exists'}

    cursor.execute('SELECT * FROM users WHERE email = %s ;', (Email,))
    if cursor.rowcount > 0:
        return {'OK': False, 'Error': 'Email already exists in system'}

    cursor.execute("INSERT INTO users(username, password, salt, email, name, family_name, state)"
                   + " VALUES ( %s, %s, %s, %s, %s, %s, FALSE);",
                   (Username, Password, Salt, Email, FirstName, LastName,))
    db.commit()
    try:
        sendEmailVerfication(Email, Username)
    except smtplib.SMTPRecipientsRefused as e:
        print("email not sent: Bad Recipient")  # inform user
        ok = False
        error = "Email address not correct"

    dict = {'OK': True}
    return dict


def login(j):
    db = db_mysql.db
    cursor = db_mysql.newCursor()

    Username = j['Username']
    Password = j['Password']
    if Username is None or Password is None:
        return {'OK': False, 'Error': "not a valid json"}

    cursor.execute(
        "SELECT * FROM users WHERE username = %s ;", (Username,))
    if cursor.rowcount <= 0:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s ;", (Username,))

    if cursor.rowcount <= 0:
        return {'OK': False, 'Error': "User doesn't exist"}

    row = cursor.fetchone()
    Salt = row['salt']
    print('salt ' + Salt)
    dbPassword = row['password']
    isActive = row['state']

    hash = hashlib.sha512()
    hash.update((Salt + Password).encode('utf-8'))
    enteredPassword = hash.hexdigest()
    print("enteredPassword " + enteredPassword + "\n" + "has " + dbPassword)
    if dbPassword == enteredPassword:
        if isActive == True:
            T = int(time.time())
            Session = secrets.token_hex(16)
            cursor = db_mysql.newCursor()
            SessionExp = datetime.datetime.now() + datetime.timedelta(days=2)
            cursor.execute(
                "INSERT INTO api_keys (username, api_key, exp_date) VALUES (%s, %s, %s);",
                (Username, Session, SessionExp))
            db.commit()
            return {'OK': True, 'api_key': Session, 'User': row}
        return {'OK': False, 'Error': "Account is not activated"}
    return {'OK': False, 'Error': "Wrong Password"}


def sendEmailVerfication(Email, Username):
    # design a user friendly email body

    db = db_mysql.db
    cursor = db_mysql.newCursor()
    import datetime
    expTime = datetime.datetime.now() + datetime.timedelta(days=1)
    Token = secrets.token_hex(16)
    cursor.execute(
        "INSERT INTO ActiviateTokens (Token, TokenExp, Username) VALUES (%s, %s, %s);",
        (Token, expTime, Username))
    db.commit()

    TokenURL = serverAddrs + "/confirm?token=" + str(Token)
    body = "متن ایمیل: \n %s" % (
        TokenURL)
    Mail.mail(Email, "no-reply: Activiate your hospital Account", body)


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

#
# def check_account_ownership(username, account_name):
#     cursor = db_mysql.newCursor()
#     cursor.execute(
#         "SELECT * FROM 'InstagramAccounts' WHERE 'Username' = %s AND 'InstagramUsername' = %s", (username, account_name))
#     if cursor.rowcount > 0:
#         return True
#     return False
