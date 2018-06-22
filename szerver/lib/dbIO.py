# -*- coding: utf-8 -*-
from pymongo import MongoClient
# MongoDB json-jában található egy objectId, ami nem feltétlenül json-barát,
# tehát ezért kell ezt a fura jsont rendes jsonné alakítani
from bson.json_util import dumps
from bson.objectid import ObjectId
from lib.config import *
from lib.colorPrint import *
COLLECTION_NAME = 'posts'

def dbCollection():
    mongo_cfg = get_config()['mongodb']
    client = MongoClient(mongo_cfg['host'], int(mongo_cfg['port']))
    db = client[mongo_cfg['db']]
    dbPrint('Sikeres kapcsolódás az adatbázishoz', newline = True)
    return db[COLLECTION_NAME]

def sendJSONToDB(Json):
    objectId = dbCollection().insert(Json)
# Nem kell adatbázis-szöveget írni, ha az ID ki van íratva, az már sikert jelent
    IdPrint(objectId)

def deleteAllData():
    dbCollection().remove({})
    dbPrint('Adatok sikeresen törölve', newline = False)

def deleteSpecifiedData(objectIdToDelete):
    dbCollection().remove({"_id":ObjectId(objectIdToDelete)})
    dbPrint('Bejegyzés sikeresen törölve', newline = False)

def getRecordNumber():
    return str(dbCollection().find({}).count())

def getAllData():
    cursor = dbCollection().find({})
    ListOfJsons = []
    for document in cursor:
        ListOfJsons.append(document)
    dbPrint('Adatok sikeresen lekérve', newline = False)
    return dumps(ListOfJsons)

def getSpecifiedWeekData(het):
    cursor = dbCollection().find({"het": int(het)})
    ListOfJsons = []
    for document in cursor:
        ListOfJsons.append(document)
    dbPrint('Adatok sikeresen lekérve', newline = False)
    return dumps(ListOfJsons)
