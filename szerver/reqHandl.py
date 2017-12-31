# -*- coding: utf-8 -*-

# Amikor valaki üzenetet küld, ez az osztály lesz  megfelelő függvénye lesz meghívva
import socket

from flask import Flask, request, Response, json
from flask_cors import CORS

from fileIO import fileIO
from errorHandl import errorHandl
from colorPrint import colorPrint

class onReceiveReq(fileIO, errorHandl):
	def onReceiveGet(self, clientIP):
		printObj = colorPrint()
		# [*] Anyaglekérés: jancsi.ip.címe.túróstáska
		# print('\n[-] Anyaglekérés: %s' %(clientIP))

		printObj.finePrint('Anyaglekérés: %s' %(clientIP))
		return self.readJSONFormFile('debug/data.json')

	def onReceivePost(self, clientIP):

		gotJSON = request.get_json()
		try:
			# [*] jancsi (jancsi.ip.címe.briós) bejegyzése:
			# print('\n[-] %s (%s) bejegyzése:' %( str(gotJSON['uname']), clientIP))

			colorPrint().finePrint('%s (%s) bejegyzése:' %(str(gotJSON['uname']), clientIP))


		except TypeError:
			errorHandl().errorHandling(clientIP)
			return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

		try:
			# Adatok kiírása
			print('--- Hét: %s' %(str(gotJSON['het'])))
			print('--- Nap: %s' %(str(gotJSON['nap'])))
			print('--- Tantárgy: %s' %(str(gotJSON['tant'])))
			print('--- Anyag: %s' %(str(gotJSON['anyag'])))

			self.writeJSONToFile('debug/data.json', gotJSON)

		except KeyError:
			errorHandl().errorHandling(clientIP)
			return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')

		except TypeError:
			errObj.errorHandling(clientIP)
			return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

		return Response(json.dumps('SUCCESS'), mimetype='application/json')
