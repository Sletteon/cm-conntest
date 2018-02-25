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

        if str(objectIdToDelete) == '<|>DELETE_ALL<|>':
            self.deleteAllData()
            colorPrint().warnPrint('Adatok törölve: %s' % (clientIP))
        else:
            self.deleteSpecifiedData(objectIdToDelete)
            colorPrint().warnPrint('1 bejegyzés (%s) törölve: %s' % (objectIdToDelete, clientIP))

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
             colorPrint().finePrint('%s (%s) bejegyzése:' %
                                    (str(gotJSON['uname']), clientIP))
            

             if str(gotJSON['pic']) != "":
                # Lekéri a mostani dátumot, időt és hasheli
                fileSavingDateTimeHash = hashlib.sha1(datetime.datetime.now().encode('utf-8')).hexdigest()

                # Elmenti a kapott kódolt képet, olyan fájlba, aminek a neve a  mostani dátum-időnek a hash-e
                self.saveToPicture(str(gotJSON['pic']), fileSavingDateTimeHash) 
                gotJSON['pic'] = fileSavingDateTimeHash 

             self.sendJSONToDB(gotJSON)

             print('--- Hét: %s' % (str(gotJSON['het'])))
             print('--- Nap: %s' % (str(gotJSON['nap'])))
             print('--- Tantárgy: %s' % (str(gotJSON['tant'])))
             print('--- Anyag: %s' % (str(gotJSON['anyag'])))

        except KeyError:
            errorHandl().errorHandling(clientIP)
            return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')

        except TypeError:
            errorHandl().errorHandling(clientIP)
            return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

        return Response(json.dumps({'SUCCESS': 'SUCCESS'}), mimetype='application/json')
