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
        # Fedora python3.6-ban TypeErrort ad, nem tetszik neki az encoding
        #with open(self._DATAPATH, 'w', encoding='utf-8') as file:
        with open(self._DATAPATH, 'w') as file:
            file.truncate()
            file.close()
