# -*- coding: utf-8 -*-
import os, logging, socket
from flask import Flask, request, Response, json
from flask_cors import CORS

# Ne látszódjanak a werkzeug (többek között HTTP-log) cuccai
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__, static_folder=os.path.join(os.environ['PWD'], 'client'))
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})

# Törölje a megnyitott fájlok tartalmát
def filetrunc():
	with open('debug/data.json', 'w', encoding='utf-8') as efile:
		efile.truncate()
		efile.close()

def onReceivePost(clientIP):
	gotJSON = request.get_json()
	# [*] jancsi (jancsi.ip.címe.briós) bejegyzése:
	try:
		print('\n[*] %s (%s) bejegyzése:' %( str(gotJSON['uname']), clientIP))
	except TypeError as e:
		print(e)
		return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')

	try:
		# Adatok kiírása
		print('--- Hét: %s' %(str(gotJSON['het'])))
		print('--- Nap: %s' %(str(gotJSON['nap'])))
		print('--- Tantárgy: %s' %(str(gotJSON['tant'])))
		print('--- Anyag: %s' %(str(gotJSON['anyag'])))

		# Adatok mentése
		with open('debug/data.json', 'a', encoding='utf-8') as file:
			json.dump(gotJSON, file, ensure_ascii=False)
			file.write('\n')

	except KeyError as e:
		print(e)
		return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')
	except TypeError as e:
		print(e)
		return Response(json.dumps({'ERROR': 'ERROR READING RECEIVED MESSAGE'}), status=400, mimetype='application/json')
	return Response(json.dumps('SUCCESS'), mimetype='application/json')

def onReceiveGet(clientIP):
	# [*] Hétlekérés: jancsi.ip.címe.túróstáska
	print('\n[*] Anyaglekérés: %s' %(clientIP))

	# Nyissa meg a fájlt, tartalmát küldje el
	with open('debug/data.json', 'r', encoding='utf-8') as file:
		#fileList = file.readlines()
		return Response("\n".join(file.readlines()))

@app.route('/', methods=['GET', 'POST'])
def index():
	# Csatlakozott kliens IP-címe
	clientIP = request.remote_addr
	if request.method == 'POST':
		return onReceivePost(clientIP)
	else:  # request.method == 'GET'
		return onReceiveGet(clientIP)

if __name__ == '__main__':
	# Ha bennhagyjuk, a rögzített bejegyzések úrjaindításkor törlődnek
	filetrunc()

	# Pozitívum, ha már itt tartunk
	# Lokális IP-cím lekérése zajlik a 'szerver fut' felirat mellett.
	try:
		print('[+] Szerver fut: %s' %( (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]))
	except:
		print('[!] Szerver fut, de nem lehetet az IP-címet megállapítani.')
	app.run(host='0.0.0.0')
