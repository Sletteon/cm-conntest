# -*- coding: utf-8 -*-
from pymongo import MongoClient

from colorPrint import colorPrint
from pymongo import MongoClient

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
