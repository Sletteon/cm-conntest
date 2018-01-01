#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#	######################################
#	cm-kapcsolatteszt szerveroldali szkript
#
# 	Flask ügye, ha ez a gép egy kérést kap, akkor futtassa le az index() függvényt.
# 	Amennyiben GET metódussal csatlakoztak kliensek erre a szerverre,
#	lekérnek adatot, így a POST metódussal beküldött adatokat,
#	JSON formában visszaszolgálja.
#	######################################

# [+] Hiba nélkül történt valami (zöld)
# [-] Semmi extra (kék)
# [*] Nem végzetes hiba (sárga)
# [&&&] Végzetes hiba (piros, alig látszik)

# Standard könyvárak
import os, logging, socket, sys

# Hozzáadott könyvárak
from flask import Flask, request, Response
from flask_cors import CORS

# Saját osztáyok
from fileIO import fileIO
from reqHandl import onReceiveReq
from colorPrint import colorPrint
from errorHandl import errorHandl

# Ne látszódjanak a werkzeug (többek között HTTP-log) cuccai
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__, static_folder=os.path.join(os.environ['PWD'], 'client'))
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})

@app.errorhandler(404)
def badRequest(e):
	return Response(errorHandl().RequestError(request, 404), status=404, mimetype='application/json')

@app.errorhandler(400)
def badRequest(e):
	return Response(errorHandl().RequestError(request, 400, errorCodeToldalek = '-as'), status=400, mimetype='application/json')

@app.errorhandler(500)
def badRequest(e):
	return Response(errorHandl().RequestError(request, 500, errorCodeToldalek = '-as'), status=500, mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
	onReceiveReqObj = onReceiveReq()
	# Csatlakozott kliens IP-címe
	clientIP = request.remote_addr
	if request.method == 'POST':
		return onReceiveReqObj.onReceivePost(clientIP)
	else:  # request.method == 'GET'
		return onReceiveReqObj.onReceiveGet(clientIP)

# Lokális Ip-t (hálózaton belülit) ad vissza
# Ha nem vagyunk online, OSError-t dob fel
def getlocalIp():
	return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]


if __name__ == '__main__':
	# Ha bennhagyjuk, a rögzített bejegyzések újraindításkor törlődnek
	fileIO().filetrunc()

	try:
		port = sys.argv[1]
		if int(port)<1000:
			colorPrint().lowPortNumberWarn()

		localIp = getlocalIp()

	except IndexError: # nincs port
		try: # van internet, nincs port
			colorPrint().startPrint(getlocalIp() + ':5000')
			try:
				app.run(host='0.0.0.0')
			except OSError:
				colorPrint().errPrint('Már el lett indítva a szerver ezen a porton')
		except OSError: # nincs internet, nincs port
			colorPrint().startPrintNoIP()
			colorPrint().okPrint('Szerver elérhető az 5000-s porton')
			try:
				app.run(host='0.0.0.0')
			except OSError:
				colorPrint().errPrint('Már el lett indítva a szerver ezen a porton')

	except ValueError: # ha a felhasználó nem érvényes portszámot adott meg
		colorPrint().notValidPortNumberErr()

	except OSError: # nincs internet, van port
		colorPrint().startPrintNoIP()
		colorPrint().okPrint('Szerver elérhető a %s-s porton' % (str(port)))
		try:
			app.run(host='0.0.0.0', port=int(port))
		except OSError:
			colorPrint().errPrint('Már el lett indítva a szerver ezen a porton')

	else: # van internet, van port
		colorPrint().startPrint('%s:%s' %(localIp, str(port)))
		try:
			app.run(host='0.0.0.0', port=int(port))
		except OSError:
			colorPrint().errPrint('Már el lett indítva a szerver ezen a porton')
