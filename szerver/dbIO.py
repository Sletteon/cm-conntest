# -*- coding: utf-8 -*-
from pymongo import MongoClient
# MongoDB json-jában található egy objectId, ami nem feltétlenül json-barát,
# tehát ezért kell ezt a fura jsont rendes jsonné alakítani
from bson.json_util import dumps
from bson.objectid import ObjectId
from config import get_config
from colorPrint import colorPrint
COLLECTION_NAME = 'posts'


class dbIO:
    def dbCollection(self):
        mongo_cfg = get_config()['mongodb']
        client = MongoClient(mongo_cfg['host'], int(mongo_cfg['port']))
        db = client[mongo_cfg['db']]
        colorPrint().dbPrint('Sikeres kapcsolódás az adatbázishoz', newline = True)
        return db[COLLECTION_NAME]

    def sendJSONToDB(self, Json):
        objectId = self.dbCollection().insert(Json)
    # Nem kell adatbázis-szöveget írni, ha az ID ki van íratva, az már sikert jelent
        colorPrint().IdPrint(objectId)
    def deleteAllData(self):
        self.dbCollection().remove({})
        colorPrint().dbPrint('Adatok sikeresen törölve', newline = False)

    def deleteSpecifiedData(self, objectIdToDelete):
        self.dbCollection().remove({"_id":ObjectId(objectIdToDelete)})
        colorPrint().dbPrint('Bejegyzés sikeresen törölve', newline = False)

    def getRecordNumber(self):
        return str(self.dbCollection().find({}).count())

    def getAllData(self):
        cursor = self.dbCollection().find({})
        ListOfJsons = []
        for document in cursor:
            ListOfJsons.append(document)
        colorPrint().dbPrint('Adatok sikeresen lekérve', newline = False)
        return dumps(ListOfJsons)

    def getSpecifiedWeekData(self, het):
        cursor = self.dbCollection().find({"het": int(het)})
        ListOfJsons = []
        for document in cursor:
            ListOfJsons.append(document)
        colorPrint().dbPrint('Adatok sikeresen lekérve', newline = False)
        return dumps(ListOfJsons)
