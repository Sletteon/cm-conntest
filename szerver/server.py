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


import os, logging, socket
from flask import Flask, request, Response, json, render_template
from flask_cors import CORS
from colorama import Fore, Style

from fileIO import fileIO
from reqHandl import onReceiveReq
from colorPrint import colorPrint

# Ne látszódjanak a werkzeug (többek között HTTP-log) cuccai
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__, static_folder=os.path.join(os.environ['PWD'], 'client'))
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})

@app.errorhandler(404)
def badRequest(error):
	colorPrint().errPrint('404-es hiba nála: %s' %(request.remote_addr))
	return Response(json.dumps({'ERROR': '404 ERROR'}), status=404, mimetype='application/json')

@app.errorhandler(400)
def badRequest(error):
	colorPrint().errPrint('400-as hiba nála: %s' %(request.remote_addr))
	return Response(json.dumps({'ERROR': '400 ERROR'}), status=400, mimetype='application/json')

@app.errorhandler(500)
def badRequest(error):
	colorPrint().errPrint('500-as hiba nála: %s' %(request.remote_addr))
	return Response(json.dumps({'ERROR': '500 ERROR'}), status=500, mimetype='application/json')

@app.route('/', methods=['GET', 'POST'])
def index():
	onReceiveReqObj = onReceiveReq()
	# Csatlakozott kliens IP-címe
	clientIP = request.remote_addr
	if request.method == 'POST':
		return onReceiveReqObj.onReceivePost(clientIP)
	else:  # request.method == 'GET'
		return onReceiveReqObj.onReceiveGet(clientIP)

if __name__ == '__main__':
	fileIOObj = fileIO()
	cp = colorPrint()
	# Ha bennhagyjuk, a rögzített bejegyzések úrjaindításkor törlődnek
	fileIOObj.filetrunc()
	# Pozitívum, ha már itt tartunk
	# Lokális IP-cím lekérése zajlik a 'szerver fut' felirat mellett.

	try:
		print(Fore.GREEN + '[+] ' + Style.RESET_ALL + 'Szerver fut: %s' %( (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]))
	except Exception as e:
		print(Fore.GREEN + '[+] ' + Style.RESET_ALL + 'Szerver fut...')
		cp.warnPrint('Nem lehetett IP-címet megállapítani')

	app.run(host='0.0.0.0')
