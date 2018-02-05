# -*- coding: utf-8 -*-
from pymongo import MongoClient
# MongoDB json-jában található egy objectId, ami nem feltétlenül json-barát,
# tehát ezért kell ezt a fura jsont rendes jsonné alakítani 
from bson import Binary, Code
from bson.json_util import dumps

from colorPrint import colorPrint


class dbIO:

    def dbCollection(self):
        client = MongoClient('192.168.1.160', 27017)
        db = client['cm']
        return db['posts']

    def sendJSONToDB(self, Json):
        objectId = self.dbCollection().insert(Json)
        # colorPrint().finePrint('Beírás: ' + str(objectId))
        print('--- Id: %s' % (objectId))

    def deleteAllData(self):
        self.dbCollection().remove({})

    def getRecordNumber(self):
        colorPrint().finePrint(self.dbCollection().find({}).count())

    def getAllData(self):
        cursor = self.dbCollection().find({})
        ListOfJsons = []
        for document in cursor:
            ListOfJsons.append(document)
        return str(dumps(ListOfJsons)).replace("'", '"')
