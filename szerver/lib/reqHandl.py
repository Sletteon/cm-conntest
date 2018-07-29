# -*- coding: utf-8 -*-

# Amikor valaki üzenetet küld, ez az osztály lesz  megfelelő függvénye lesz meghívva
import socket
import datetime
import hashlib
import json

from flask import Flask, request, Response
from flask_cors import CORS

from lib.errorHandl import *
from lib.colorPrint import *
from lib.dbIO import *

def onReceiveMotd(clientIP):
    # csak az első sort adjuk vissza
    with open('motd.txt', 'r', encoding='utf-8') as file:
        return file.readline().strip()   

def onReceiveDelete(clientIP, objectIdToDelete):

    if str(objectIdToDelete) == '*':
        warnPrint('Adatok törlése: %s' % (clientIP))
        deleteAllData()
    else:
        warnPrint('1 bejegyzés (%s) törlése: %s' % (objectIdToDelete, clientIP))
        deleteSpecifiedData(objectIdToDelete)

    return Response(json.dumps({'SUCCESS': 'SUCCESS'}), mimetype='application/json')

def onReceiveGet(clientIP):
    # [*] Anyaglekérés: jancsi.ip.címe.túróstáska
    finePrint('Mindegyik hét lekérése: %s' % (clientIP))
    # return readJSONFormFile(fileIO().dataDotJsonPath)
    return getAllData()

def onReceiveSpecifiedGet(clientIP, het):
    finePrint('%s.hét lekérése: %s' % (het, clientIP))

    return getSpecifiedWeekData(het)

def onReceiveRecordNumberGet(clientIP):
    finePrint('Adatok számának lekérése: %s' % (clientIP))
    return getRecordNumber()

def onReceivePost(clientIP):

    gotJSON = request.get_json()

    # stringet kapunk, ha több bejegyzés érkezik
    if type(gotJSON).__name__ == 'str':
        gotJSONList = json.loads(gotJSON)
        finePrint('%s (%s) bejegyzéseket (%s db) küldött' %
                                (str(gotJSONList[0]['uname']), clientIP, len(gotJSONList)))
        sendMultipleJSONsToDB(gotJSONList)
        return Response(json.dumps({'SUCCESS': 'SUCCESS'}), mimetype='application/json')
    try:
         finePrint('%s (%s) bejegyzést küldött' %
                                (str(gotJSON['uname']), clientIP))
       
         # Ha nem létezik kép, akkor is hozzon létre kép kulcsot üres stringgel
         try:
             if str(gotJSON['pic']) != '':
                 picExists = True
                 pass
             else:
                 picExists = False
         except KeyError:
             gotJSON['pic'] = ''
             picExists = False

         sendJSONToDB(gotJSON)

         #print('--- hét: {}'.format(str(gotjson['het'])))
         #print('--- nap: {}'.format(str(gotjson['nap'])))
         #print('--- tantárgy: {}'.format(str(gotjson['tant'])))
         #print('--- anyag: {}'.format(str(gotjson['anyag'])))
         #print('--- kép: {}'.format('van' if str(gotjson['pic']) != '' else 'nincs'))
         week = str(gotJSON['het'])
         day = str(gotJSON['nap'])
         subj = str(gotJSON['tant'])
         mat = str(gotJSON['anyag'])
         pic = 'van' if str(gotJSON['pic']) != '' else 'nincs'
         gotDataPrint(week, day, subj, mat, pic)
        
    except KeyError:
        errorHandling(clientIP)
        return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')

    except TypeError:
        errorHandling(clientIP)
        return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

    return Response(json.dumps({'SUCCESS': 'SUCCESS'}), mimetype='application/json')
