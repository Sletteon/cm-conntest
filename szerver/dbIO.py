# -*- coding: utf-8 -*-
from pymongo import MongoClient
# MongoDB json-jában található egy objectId, ami nem feltétlenül json-barát,
# tehát ezért kell ezt a fura jsont rendes jsonné alakítani
from bson.json_util import dumps
from config import get_config

COLLECTION_NAME = 'posts'


class dbIO:
    def dbCollection(self):
        mongo_cfg = get_config()['mongodb']
        client = MongoClient(mongo_cfg['host'], int(mongo_cfg['port']))
        db = client[mongo_cfg['db']]
        return db[COLLECTION_NAME]

    def sendJSONToDB(self, Json):
        objectId = self.dbCollection().insert(Json)
        # colorPrint().finePrint('Beírás: ' + str(objectId))
        print('--- Id: %s' % (objectId))

    def deleteAllData(self):
        self.dbCollection().remove({})

    def getRecordNumber(self):
        return str(self.dbCollection().find({}).count())

    def getAllData(self):
        cursor = self.dbCollection().find({})
        ListOfJsons = []
        for document in cursor:
            ListOfJsons.append(document)
        return str(dumps(ListOfJsons)).replace("'", '"')

    def getSpecifiedWeekData(self, het):
        cursor = self.dbCollection().find({"het": int(het)})
        ListOfJsons = []
        for document in cursor:
            ListOfJsons.append(document)
        return str(dumps(ListOfJsons)).replace("'", '"')
