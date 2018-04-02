#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import hashlib
import sys
import time
import base64
import os

from random import randint

# Ahogy a neve is utal rá, visszaadja a fájlok tartalmát stringben
def fileToBase64(filePath):
    with open(filePath, 'rb') as fileObj:
        return base64.b64encode(fileObj.read())

# Mindenesetben egy 'http://{}:5000'-t kérünk, ha nincs így megadva, akkor egészítsük ki
try:
    ServerIp = sys.argv[1]
    if {":", "."}.issubset(ServerIp):
        ServerAddr = ServerIp.split(":")
        fullServerAddr = 'http://' + ServerAddr[0] + ':' + ServerAddr[1]
    else:
        if "." not in ServerIp and 'localhost' not in ServerIp:
            print('<!> Hibás hostname vagy IP-cím')
            exit()
        fullServerAddr = 'http://{}:5000'.format(ServerIp)

except IndexError:
    print('<!> Nincs IP-cím szolgáltatva, kilépés')
    exit()

# Ha van kép szolgáltatva, írjuk ki, mennyi adatot fogunk átküldeni, majd állítsuk be a pic változót a kódolt képre
try:
    picPath = sys.argv[2]
    pic = str(fileToBase64(picPath))
    picSize = os.path.getsize(picPath)
    print('(i) {} MB-nyi adatforgalomra kell számítani (beküldés + ÖSSZES adatbázisban lévő kép)\n'.format(str(round(picSize*1000/1048576, 2)*2)))
except IndexError:
    pic = ''


# 1000 hosszú json-t küld be, ami egy (egyáltalán nem) realisztikus terhelést törekszik elérni
print('[*] Beállítás-teszt\n')

nap = ('H', 'K', 'S', 'C', 'P')

start = time.time()
for i in range(1001):
    try:
        generatedHet = randint(0, 52)
        generatedNap = randint(0, len(nap) - 1)

        r = requests.post(fullServerAddr, json={
            'uname': 'TEST_NUMBER_' + str(i),
            'het': generatedHet,
            'nap': nap[generatedNap],
            'tant': hashlib.sha1(str(i + generatedHet * generatedNap).encode('utf-8')).hexdigest(),
            'anyag': hashlib.md5(str(i + generatedHet * generatedNap).encode('utf-8')).hexdigest(),
            'pic': pic
        })
    # Hibák elkapása
        r.raise_for_status()
    except requests.exceptions.HTTPError as httperr:
        print('<!> ' + str(httperr))
        exit(1)
    except requests.exceptions.RequestException as e:
        print('<!> ' + str(e))
        exit(1)

    if not r.json() == {'SUCCESS': 'SUCCESS'} and not i == 0:
        raise EnvironmentError('<!> Szerver rossz választ adott')
        exit(1)
    else:
        if not r.json() == {'SUCCESS': 'SUCCESS'}:
            raise EnvironmentError('<!> Hibás beállítás')
            exit(1)

if i == 1000:
    print('[+] Sikeres beállítás-teszt\n')
    print('[*] ' + str(i) + ' beküldés ' + str(time.time() - start)[:5] + ' mp alatt lett feldolgozva\n')
    print('[*] Lekérés\n')
    try:
        r = requests.get(fullServerAddr)
        r.raise_for_status()
        if r.text is not None and not r.text == '':
            print('[+] Sikeres lekérés')
        else:
            raise EnvironmentError('<!> Üres válasz a lekérésre')
            exit(1)
    except requests.exceptions.HTTPError as httperr:
        print('<!> ' + str(httperr))
        exit(1)
