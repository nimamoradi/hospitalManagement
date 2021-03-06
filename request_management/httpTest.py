# -*- coding: utf-8 -*-
import os
import string
from bottle import Bottle, get, post, route, run, template, request, hook, response

import request_management
from rbac.roles import api_key_to_user, permission
from rbac.roles import roles as user_group
from request_management.user import signing, profile
from request_management.chat import chat
from request_management.accounting import accounting


# import cronJobs
# import botManager
from request_management import db_mysql
from request_management.user.dotor_func import search_doctor
from request_management.user.reservation import reserve_doctor_time
import request_management.user.receptor
import request_management.pharmacy.medicine

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
# @get('/confirm')
# def index():
#     dict = confirmEmail()
#     return dict


@post('/search_medicine', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine.search_medicine(j['name'])


@post('/add_medicine', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine.add_medicine(j['name'], j['price'], j['exp_date'])


@post('/get_medicine', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine.get_medicine(j['id'])


@post('/get_prescription_details', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine. \
        get_prescription_details(j['ids'])


@post('/update_medicine', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine.update_medicine(j['id'], j['price'], j['exp_date'])


@post('/get_medicine_bydate', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine.get_medicine_bydate()


@post('/reserve_doctor_time', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    if 'reserve_id' in j:
        dict = reserve_doctor_time(j['reserve_id'], j['patient_username'])
    else:
        return "error: missing param"
    return dict


@post('/search_doctor', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    if 'username' in j and len(j['username']) > 2:
        dict = search_doctor(j['username'])
    else:
        return "error: missing param"
    return dict


@post('/see_doctor_times', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    dict = request_management.user.reservation.see_doctor_times(j['username'])
    return dict


@post('/see_doctor_times_receptor', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    dict = request_management.user.receptor.see_doctor_times(j['username'])
    return dict


@post('/cancel_reserve', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    request_management.user.receptor.cancel_reserve(j['reserve_id'])
    return request_management.user.receptor.see_doctor_times(j['username'])


@post('/doctor_accept_reserve', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.user.dotor_func.accept_reserve(j['reserve_id'], j['username'])


@post('/add_doctor_time', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.user.receptor.add_doctor_time(
        j['doctor_username'], j['week_day'], j['hour'], j['price'])


@post('/delete_doctor_time', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.user.receptor.delete_doctor_time(
        j['id'])


@post('/doctor_prescribe', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.user.dotor_func.prescribe(j['patient_id'], j['username'],
                                                        j['prescription'])


@post('/doctor_cancel_reserve', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    request_management.user.dotor_func.cancel_reserve(j['reserve_id'], j['username'])
    return request_management.user.receptor.see_doctor_times(j['username'])


@post('/get_patient_history', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    api_key = api_key_to_user(j['api_key'])
    if api_key['OK'] and permission(api_key['user']['role'], ['doctor', 'admin']):
        return request_management.user.dotor_func.get_medicine_history(j['patient_username'])
    else:
        return {'OK': False, 'Error': 'no permission'}


@post('/patient_hospitalize', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.user.dotor_func.hospitalize(j['patient_username'], j['doctor_username'])


@post('/get_user_prescription', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.pharmacy.medicine.get_user_prescription(j['patient_username'])


@route('/login', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    dict = signing.login(j)
    return dict  # send api result as json, no need to encode


@route('/register', method=['POST', 'OPTIONS'])
def index():
    # TODO XSS safe the input
    # print("request" + str(request.json))
    if not request.json:
        return "error: not a json"

    j = request.json
    dict = signing.register(j)

    return dict  # send api result as json, no need to encode


@route('/forget', method=['POST', 'OPTIONS'])
def index():
    # TODO XSS safe the input
    # print("request" + str(request.json))
    if not request.json:
        return "error: not a json"
    j = request.json
    dict = signing.forget_password(j)

    return dict  # send api result as json, no need to encode


@post('/show_res', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"
    j = request.json
    return request_management.user.dotor_func.show_result(j['patient_id'], j['username'],
                                                        j['prescription'])



@route('/edit_profile', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = profile.edit_profile(j)
    return dict  # send api result as json, no need to encode


@route('/send_message', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = chat.send_message(j)
    return dict  # send api result as json, no need to encode


@route('/get_messages', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = chat.get_messages(j)
    return dict  # send api result as json, no need to encode


@route('/get_invoice', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = accounting.get_invoice(j)
    return dict  # send api result as json, no need to encode


@route('/pay', method=['POST', 'OPTIONS'])
def index():
    if not request.json:
        return "error: not a json"

    j = request.json

    dict = accounting.pay(j)
    return dict  # send api result as json, no need to encode


# @route('/json', method=['POST', 'OPTIONS'])
# def index():
#     if not request.json:
#         return "error: not a json"

#     j = request.json
#     print("hello from json")

#     log = {'Name': 'Zara', 'title': "pro", 'Class': 'First'}
#     return log  # a # send api result as json, no need to encode


# @post('/json2/<user>')  # also we can get url parameters
# def index(user):
#     j = request.json
#     a = {'a': 0, 'b': 1}
#     a['title'] = j['title']
#     a['user'] = user  # use url parameters like this
#     return a


# @route('/uploadPhoto', method=['POST', 'OPTIONS'])
# def do_upload():
#     account_name = request.forms.get('account_name')
#     session = request.forms.get('Session')
#     time_stamp = request.forms.get('TimeStamp')
#     caption = request.forms.get('Caption')
#
#     # check for login and account owner ship
#     Username = check_login(session)
#     if Username == False:
#         return {'OK': False, 'Error': "You are not logged in"}
#
#     if not check_account_ownership(Username, account_name):
#         return {'OK': False, 'Error': "Not your Account"}
#
#     try:
#         upload = request.files.get('upload')
#         name, ext = os.path.splitext(upload.filename)
#         if ext not in ('.jpg'):
#             return "File extension not allowed."
#         # check if folder exists
#         if not os.path.exists("./Photos"):
#             os.makedirs("./Photos")
#         # generate a random string for files with same name
#         rand = ''.join([random.choice(string.ascii_letters + string.digits)
#                         for n in range(10)])
#         file_path = "Photos/{file}".format(file=Username +
#                                                 "-" + rand + upload.filename)
#         upload.save(file_path)
#
#         cursor = db_mysql.newCursor()
#         cursor.execute(
#             "INSERT INTO 'Photos'('Username', 'PhotoName', 'PhotoCaption', 'PostTime') VALUES (%s, %s, %s, %s)",
#             (Username, file_path, caption, time_stamp))
#
#     except Exception as e:
#         return "somthing went wrong"
#
#     return "File successfully saved "


# def confirmEmail():
#     Token = str(request.GET.get('token', '').strip())
#     db = db_mysql.db
#     cursor = db_mysql.newCursor()
#     cursor.execute(
#         "SELECT * FROM ActiviateTokens WHERE Token = %s;", (Token,))
#     if cursor.rowcount <= 0:
#         return {'OK': False, 'Error': 'Incorrect Token'}

#     row = cursor.fetchone()
#     Username = row['Username']
#     TokenExp = row['TokenExp']
#     import datetime
#     if TokenExp < datetime.datetime.now():
#         return {'OK': False, 'Error': 'Expired Token'}

#     cursor = db_mysql.newCursor()
#     cursor.execute(
#         "UPDATE Users SET state = True WHERE Username = %s", (Username,))
#     cursor.execute(
#         "DELETE FROM ActiviateTokens WHERE Username = %s", (Username,))
#     db.commit()

#     dict = {'OK': True}
#     return dict

#
# def check_account_ownership(username, account_name):
#     cursor = db_mysql.newCursor()
#     cursor.execute(
#         "SELECT * FROM 'InstagramAccounts' WHERE 'Username' = %s AND 'InstagramUsername' = %s", (username, account_name))
#     if cursor.rowcount > 0:
#         return True
#     return False
