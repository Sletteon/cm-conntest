#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, sys

for i in range(1001):
	r = requests.post('http://46.139.116.9:5000',json={'uname':'TESTNUMBER' + str(i), 'het':'E', 'nap':'P', 'tant':'NagyonHosszúTantárgyÉkezetekÉsEsetlegesEgyébProblémákTesztelésére', 'anyag':'AnyagNumber'+str(i)})
	if not r.json() == 'SUCCESS' and not i == 0 :
		raise ServerError('Szerver lefagyott')
	else:
		if not r.json() == 'SUCCESS':
			raise ServerError('Rosszul lett valami beállítva')
