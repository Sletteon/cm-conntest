#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, hashlib
from random import randint

# 1000 hosszú json-t küld be, ami egy (túl)realisztikus terhelést törekszik elérni
print('[*] Beállítás-teszt')

nap = ('H', 'K', 'S', 'C', 'P')
het = ('E', 'J')

for i in range(1001):
	try:
		r = requests.post('http://46.139.116.9:5000',json={
						'uname':'TEST_NUMBER_' + str(i),
						'het':het[randint(0,1)], 'nap':nap[randint(0,4)],
						'tant': hashlib.sha1(str(i).encode('utf-8')).hexdigest(),
						'anyag': hashlib.md5(str(i).encode('utf-8')).hexdigest()
						})
		r.raise_for_status()
	except requests.exceptions.HTTPError as httperr:
		print('<!> ' + str(httperr))
		exit(1)
	except requests.exceptions.RequestException as e:
		print('<!> ' + str(e))
		exit(1)

	if not r.json() == 'SUCCESS' and not i == 0 :
		raise EnvironmentError('<!> Szerver rossz választ adott')
		exit(1)
	else:
		if not r.json() == 'SUCCESS':
			raise EnvironmentError('<!> Hibás beállítás')
			exit(1)

if i == 1000:
	print('[+] Sikeres beállítás-teszt')
	print('[*] Lekérés')
	try:
		r = requests.get('http://46.139.116.9:5000')
		r.raise_for_status()
		if not r.text == None and not r.text == '':
			print('[+] Sikeres lekérés')
		else:
			raise EnvironmentError('<!> Üres válasz a lekérésre')
			exit(1)
	except requests.exceptions.HTTPError as httperr:
		print('<!> ' + str(httperr))
		exit(1)
