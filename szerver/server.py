# -*- coding: utf-8 -*-
import os, logging, socket
from flask import Flask, request, Response, json
from flask_cors import CORS

# Ne látszódjanak a werkzeug (többek között HTTP-log) cuccai
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

STATIC_FOLDER = os.path.join(os.environ['PWD'], 'client')
app = Flask(__name__, static_folder = STATIC_FOLDER)
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})

# Törölje a megnyitott fájlok tartalmát
def filetrunc():
	with open('debug/data.json', 'w') as efile:
		efile.truncate()
		efile.close()

@app.route('/', methods=['GET', 'POST'])
def index():
	clientIP = request.remote_addr
	if request.method == 'POST':
		gotJSON = request.get_json()
		# [*] jancsi (jancsi.ip.címe.briós) bejegyzése:
		print('\n' + '[*] ' + str(gotJSON['uname']) + ' (' + clientIP + ')' + ' bejegyzése: ')
		# Próbálja meg a beküldött adatot (JSON) szétválasztani,
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

		# Adatok mentése
		with open('debug/data.json', 'a') as file:
			json.dump(gotJSON, file)
			file.write('\n')

		return Response(json.dumps('SUCCESS'), mimetype='application/json')
	else: #request.method == 'GET'
		# [*] Hétlekérés: jancsi.ip.címe.túróstáska
		print('\n' + '[*] Anyaglekérés: ' + clientIP)

		# Nyissa meg a fájlt, tartalmát küldje el
		with open('debug/data.json', 'r') as file:
			fileList = file.readlines()
			return Response("\n".join(fileList))

if __name__ == '__main__':
	# Ha bennhagyjuk, a rögzített bejegyzések úrjaindításkor törlődnek
	filetrunc();

	# Pozitívum, ha már itt tartunk
	# Lokális IP-cím lekérése zajlik a szerver fut felirat mellett.
	print('[+] Szerver fut: ' + (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
	app.run(host='0.0.0.0')
