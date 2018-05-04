# -*- coding: utf-8 -*-

# Amikor valaki üzenetet küld, ez az osztály lesz  megfelelő függvénye lesz meghívva
import socket
import datetime
import hashlib

from flask import Flask, request, Response, json
from flask_cors import CORS

from fileIO import fileIO
from errorHandl import errorHandl
from colorPrint import colorPrint
from dbIO import dbIO


class onReceiveReq(fileIO, errorHandl, dbIO):

    def onReceiveDelete(self, clientIP, objectIdToDelete):

        if str(objectIdToDelete) == '*':
            colorPrint().warnPrint('Adatok törlése: %s' % (clientIP))
            self.deleteAllData()
        else:
            colorPrint().warnPrint('1 bejegyzés (%s) törlése: %s' % (objectIdToDelete, clientIP))
            self.deleteSpecifiedData(objectIdToDelete)

        return Response(json.dumps({'SUCCESS': 'SUCCESS'}), mimetype='application/json')

    def onReceiveGet(self, clientIP):
        printObj = colorPrint()
        # [*] Anyaglekérés: jancsi.ip.címe.túróstáska
        printObj.finePrint('Mindegyik hét lekérése: %s' % (clientIP))
        # return self.readJSONFormFile(fileIO().dataDotJsonPath)
        return self.getAllData()

    def onReceiveSpecifiedGet(self, clientIP, het):
        colorPrint().finePrint('%s.hét lekérése: %s' % (het, clientIP))

        return self.getSpecifiedWeekData(het)

    def onReceiveRecordNumberGet(self, clientIP):
        colorPrint().finePrint('Adatok számának lekérése: %s' % (clientIP))
        return self.getRecordNumber()

    def onReceivePost(self, clientIP):

        gotJSON = request.get_json()
        try:
             colorPrint().finePrint('%s (%s) bejegyzést küldött' %
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

             self.sendJSONToDB(gotJSON)

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
             colorPrint().gotDataPrint(week, day, subj, mat, pic)
            
        except KeyError:
            errorHandl().errorHandling(clientIP)
            return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')

        except TypeError:
            errorHandl().errorHandling(clientIP)
            return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

        return Response(json.dumps({'SUCCESS': 'SUCCESS'}), mimetype='application/json')
