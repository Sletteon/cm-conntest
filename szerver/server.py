# -*- coding: utf-8 -*-
import os, logging
from flask import Flask, request, Response, json
from flask_cors import CORS

# Ne látszódjanak a werkzeug cuccai
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

STATIC_FOLDER = os.path.join(os.environ['PWD'], 'client')
# app objektum
app = Flask(__name__, static_folder = STATIC_FOLDER)
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})

# Ezzel választja el a fájlokban az adatokat
separatorChar = '<|>'

# Töröjle a megnyitott fájlok tartalmát
def filetrunc():
	with open('debug/E.ssv', 'a+') as efile:
		efile.truncate()
		efile.close()

	with open('debug/J.ssv', 'a+') as jfile:
		jfile.truncate()
		jfile.close()


@app.route('/', methods=['GET', 'POST'])
def index():
	IP = request.remote_addr
	if request.method == 'POST':
		gotJSON = request.get_json()
		# [*] jancsi (jancsi.ip.kakaós.csiga) bejegyzése:
		print('\n' + '[*] ' + str(gotJSON['uname']) + ' (' + IP + ')' + ' bejegyzése: ')
		# próbálja meg a beküldött adatot (JSON) szétválasztani,
		# lokális változókat létrehozva
		try:
			uname = gotJSON['uname']
			het = gotJSON['het']
			nap = gotJSON['nap']
			tant = gotJSON['tant']
			anyag = gotJSON['anyag']
		except KeyError:
			response = json.dumps({'error': 'Missing input parameter'})
			return Response(response, status=422, mimetype='application/json')

		# Adatok kiírása
		print('--- Hét: ' + str(het))
		print('--- Nap: ' + str(nap))
		print('--- Tantárgy: ' + str(tant))
		print('--- Anyag: ' + str(anyag))

		# Adatok mentése a megfelelő fájlba
		if het == 'E':
			with open('debug/E.ssv', 'a+') as efile:
				efile.write(separatorChar.join([uname, het, nap, tant, anyag]) + '\n')
		if het == 'J':
			with open('debug/J.ssv', 'a+') as jfile:
				jfile.write(separatorChar.join([uname, het, nap, tant, anyag]) + '\n')
		return Response(json.dumps('SUCCESS'), mimetype='application/json')
	else: #request.method == 'GET'
		# [*] Hétlekérés: jancsi.ip.lekváros.kenyér
		print('\n' + '[*] Hétlekérés: ' + IP)

		# Átmeneti (szörnyű) megoldás: hozzon létre változókat,
		# ha nincs pl. a jövő heti fájlba írva semmi,
		# akkor is küldje el a jövő heti fájl kulcsait, '' értékkel
		unameE, hetE, napE, tantE, anyagE, unameJ, hetJ, napJ, tantJ, anyagJ = '' , '' , '' , '' , '' , '' , '' , '' , '' , ''
		# Nyissa meg a fájlokat, írja a memóriába a változókat
		with open('debug/E.ssv', 'a+') as efile:
			line = efile.readline()
			if line != '' and separatorChar in line:
				unameE, hetE, napE, tantE, anyagE = line.strip().split(separatorChar)

		with open('debug/J.ssv', 'a+') as jfile:
			line = jfile.readline()
			if line != '' and separatorChar in line:
				unameJ, hetJ, napJ, tantJ, anyagJ = line.strip().split(separatorChar)

		returnJSON = {
			'E':
			{
				'uname': unameE,
				'het': hetE,
				'nap': napE,
				'tant': tantE,
				'anyag': anyagE
			},
			'J':
			{
				'uname': unameJ,
				'het': hetJ,
				'nap': napJ,
				'tant': tantJ,
				'anyag': anyagJ
			}
		}

		return Response(json.dumps(returnJSON))

if __name__ == '__main__':
	# Ha bennhagyjuk, leállításig rögzített bejegyzések úrjaindításkor törlődnek
	filetrunc();
	# Pozitívum, ha már itt tartunk
	print('[+] Szerver fut')
	app.run(host='0.0.0.0')
