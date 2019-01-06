import time
from reqest_mangment import httpTest


def main():

    try:
        httpTest.run(host='localhost', port=2228)
    except Exception as e:
        print ("somthing went a whole wrong")


