#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, hashlib, sys, time
from random import randint

try:
    ServerIp = sys.argv[1]
except IndexError:
    ServerIp = '46.139.116.9'

# 1000 hosszú json-t küld be, ami egy (egyáltalán nem) realisztikus terhelést törekszik elérni
print('[*] Beállítás-teszt\n')

nap = ('H', 'K', 'S', 'C', 'P')
het = ('E', 'J', 'EE', 'JU')

start = time.time()
for i in range(1001):
    try:
        generatedHet = randint(0, 52)
        generatedNap = randint(0, len(nap) - 1)
        r = requests.post('http://' + ServerIp + ':5000', json={
            'uname': 'TEST_NUMBER_' + str(i),
            'het': generatedHet,
            'nap': nap[generatedNap],
            'tant': hashlib.sha1(str(i + generatedHet * generatedNap).encode('utf-8')).hexdigest(),
            'anyag': hashlib.md5(str(i + generatedHet * generatedNap).encode('utf-8')).hexdigest()
        })
        r.raise_for_status()
    except requests.exceptions.HTTPError as httperr:
        print('<!> ' + str(httperr))
        exit(1)
    except requests.exceptions.RequestException as e:
        print('<!> ' + str(e))
        exit(1)

    if not r.json() == 'SUCCESS' and not i == 0:
        raise EnvironmentError('<!> Szerver rossz választ adott')
        exit(1)
    else:
        if not r.json() == 'SUCCESS':
            raise EnvironmentError('<!> Hibás beállítás')
            exit(1)

if i == 1000:
    print('[+] Sikeres beállítás-teszt\n')
    print('[*] ' + str(i) + ' beküldés ' + str(time.time() - start)[:5] + ' mp alatt lett feldolgozva\n')
    print('[*] Lekérés\n')
    try:
        r = requests.get('http://' + ServerIp + ':5000')
        r.raise_for_status()
        if not r.text == None and not r.text == '':
            print('[+] Sikeres lekérés')
        else:
            raise EnvironmentError('<!> Üres válasz a lekérésre')
            exit(1)
    except requests.exceptions.HTTPError as httperr:
        print('<!> ' + str(httperr))
        exit(1)
