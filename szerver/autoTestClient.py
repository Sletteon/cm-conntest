#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

# 1000 hosszú json-t küld be, ami egy realisztikus terhelést törekszik elérni
for i in range(1001):
	try:
		r = requests.post('http://46.139.116.9:5000',json={'uname':'TESTNUMBER' + str(i), 'het':'E', 'nap':'P', 'tant':'NagyonHosszúTantárgyÉkezetekÉsEsetlegesEgyébProblémákTesztelésére', 'anyag':'EgyRandomAnyagAmitPárRandomÉkezetesBetűKövet:öüóőúáűíÖÜÓŐÚÁŰÍéÉ\|Ä<äđĐłŁ$ß¤'})
		r.raise_for_status()
	except requests.exceptions.HTTPError as httperr:
		print(httperr)
		exit(1)
	except requests.exceptions.RequestException as e:
		print(e)
		exit(1)

	if not r.json() == 'SUCCESS' and not i == 0 :
		raise ServerError('[!] Szerver rossz választ adott')
	else:
		if not r.json() == 'SUCCESS':
			raise ServerError('[!] Hibás beállítás')
	if r.json() == 'SUCCESS':
		print(str(i) + '. teszt sikeres')

print('[*] Vége a beírás-tesztnek, lekérés következik')
try:
	r = requests.get('http://46.139.116.9:5000')
	r.raise_for_status()
	if not r.text == None and not r.text == '':
		print('[+] Sikeres lekérés')
	else:
		raise ServerError('[!] Üres válasz a lekérésre')
except requests.exceptions.HTTPError as httperr:
	print(httperr)
	exit(1)
