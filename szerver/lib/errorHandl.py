# -*- coding: utf-8 -*-

# Később nem fogja kiírni a hibát, hanem egy logfile-ba jegyzi be
import traceback
from lib.colorPrint import *
import json


def errorHandling(clientIP):
    errPrint(
        'Hiba történt egy kliensnél (%s):\n---------------traceback---------------' % (clientIP))
    print(traceback.format_exc())
    print('---------------traceback---------------')

# Amennyiben egy http-hibát találunk, (szépen) írjuk ki, valamint küldjünk vissza egy választ a hibakóddal
def RequestError(requestObj, errorCode, errorCodeToldalek='-es'):
    errPrint('%s%s hiba nála: %s' %
                          (str(errorCode), str(errorCodeToldalek), str(requestObj.remote_addr)))
    return json.dumps({'ERROR': str(errorCode) + ' ERROR'})
