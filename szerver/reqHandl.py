# -*- coding: utf-8 -*-
import os, logging, socket, traceback
from flask import Flask, request, Response, json
from flask_cors import CORS
from fileIO import fileIO

class onReceiveReq(fileIO):
	def onReceiveGet(self, clientIP):
		# [*] Hétlekérés: jancsi.ip.címe.túróstáska
		print('\n[*] Anyaglekérés: %s' %(clientIP))
		return self.readJSONFormFile('debug/data.json')

	def onReceivePost(self, clientIP):
		# Fancy módon írja ki, hogy mi a hiba
		# Megjegyzés: azért traceback, mert az megmutatja a sorszámot,
		# ahol a hiba keletkezett
		def errorHandling(self, clientIP):
			print('\n[&&&] Hiba történt egy kliensnél (%s):\n---------------traceback---------------' %(clientIP))
			print(traceback.format_exc())
			print('---------------traceback---------------')

		gotJSON = request.get_json()
		try:
			# [*] jancsi (jancsi.ip.címe.briós) bejegyzése:
			print('\n[-] %s (%s) bejegyzése:' %( str(gotJSON['uname']), clientIP))

		except TypeError:
			errorHandling(clientIP)
			return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

		try:
			# Adatok kiírása
			print('--- Hét: %s' %(str(gotJSON['het'])))
			print('--- Nap: %s' %(str(gotJSON['nap'])))
			print('--- Tantárgy: %s' %(str(gotJSON['tant'])))
			print('--- Anyag: %s' %(str(gotJSON['anyag'])))
			
			self.writeJSONToFile('debug/data.json', gotJSON)

		except KeyError:
			self.errorHandling(clientIP)
			return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')

		except TypeError:
			self.errorHandling(clientIP)
			return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

		return Response(json.dumps('SUCCESS'), mimetype='application/json')
