# -*- coding: utf-8 -*-

# Fájlokkal zsonglőrködik
import json
import os
import hashlib
import base64

class fileIO:
    _SCRPITPATH = os.path.dirname(__file__)
    _DATAPATH = os.path.join(_SCRPITPATH, 'debug', 'data.json')
    _SEPARATOR = "<|>MEZOPOTÁMIA<|>"

    # JSON adatok mentése
    def writeJSONToFile(self, file, JSON):
        with open(file, 'a', encoding='utf-8') as fileobj:
            json.dump(JSON, fileobj, ensure_ascii=False)
            fileobj.write('\n')

    def readJSONFormFile(self, file):
        with open(file, 'r', encoding='utf-8') as file:
            return '\n'.join(file.readlines())

    def filetrunc(self):
        with open(self._DATAPATH, 'w', encoding='utf-8') as file:
            file.truncate()
            file.close()

    def saveToPicture(self, base64encodedPic, filename):
        #filename = hashlib.sha1(base64encodedPic.encode('utf-8')).hexdigest()
        picList = base64encodedPic.split(self._SEPARATOR)
        with open(filename, "wb") as fileobj:
            for picture in picList:
                fileobj.write(picture)

    def picToBinary(self, picture):
        return base64.b64encode(picture.read())

