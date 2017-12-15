# -*- coding: utf-8 -*-
import os, logging
from flask import Flask, request, Response, json
from flask_cors import CORS

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

STATIC_FOLDER = os.path.join(os.environ['PWD'], 'client')
app = Flask(__name__, static_folder = STATIC_FOLDER)
CORS(app, resources={r'/*': {'origins': '*'}})

SEPARATOR = '<|>'


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
		print('\n' + '[+] ' + str(gotJSON['uname']) + ' (' + IP + ')' + ' bejegyzése: ')
		try:
			uname = gotJSON['uname']
			het = gotJSON['het']
			nap = gotJSON['nap']
			tant = gotJSON['tant']
			anyag = gotJSON['anyag']
		except KeyError:
			response = json.dumps({'error': 'Missing input parameter'})
			return Response(response, status=422, mimetype='application/json')
		print('--- Hét: ' + str(het))
		print('--- Nap: ' + str(nap))
		print('--- Tantárgy: ' + str(tant))
		print('--- Anyag: ' + str(anyag))
		if het == 'E':
			with open('debug/E.ssv', 'a+') as efile:
				efile.write(SEPARATOR.join([uname, het, nap, tant, anyag]) + '\n')
		if het == 'J':
			with open('debug/J.ssv', 'a+') as jfile:
				jfile.write(SEPARATOR.join([uname, het, nap, tant, anyag]) + '\n')
		return Response(json.dumps('SUCCESS'), mimetype='application/json')
	else: #request.method == 'GET'
		print('\n' + '[+] Hétlekérés: ' + IP)
		unameE, hetE, napE, tantE, anyagE, unameJ, hetJ, napJ, tantJ, anyagJ = '' , '' , '' , '' , '' , '' , '' , '' , '' , ''
		with open('debug/E.ssv', 'a+') as efile:
			line = efile.readline()
			if line != '' and SEPARATOR in line:
				unameE, hetE, napE, tantE, anyagE = line.strip().split(SEPARATOR)

		with open('debug/J.ssv', 'a+') as jfile:
			line = jfile.readline()
			if line != '' and SEPARATOR in line:
				unameJ, hetJ, napJ, tantJ, anyagJ = line.strip().split(SEPARATOR)

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
	filetrunc();
	print('[+] Szerver fut')
	app.run(host='0.0.0.0')
