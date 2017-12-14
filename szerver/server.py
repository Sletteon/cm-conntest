import os
from flask import Flask, request, Response, json
from flask_cors import CORS

STATIC_FOLDER = os.path.join(os.environ['PWD'], 'client')
app = Flask(__name__, static_folder = STATIC_FOLDER)
CORS(app, resources={r"/*": {"origins": "*"}})

SEPARATOR = '<|>'


def filetrunc():
	with open("debug/E.ssv", "a+") as efile:
		efile.truncate()
		efile.close()

	with open("debug/J.ssv", "a+") as jfile:
		jfile.truncate()
		jfile.close()


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		gotJSON = request.get_json()
		print(gotJSON)
		try:
			uname = gotJSON['uname']
			het = gotJSON['het']
			nap = gotJSON['nap']
			tant = gotJSON['tant']
			anyag = gotJSON['anyag']
		except KeyError:
			response = json.dumps({'error': 'Missing input parameter'})
			return Response(response, status=422, mimetype='application/json')
		print(uname)
		print(het)
		print(nap)
		print(tant)
		print(anyag)

		if het == "E":
			with open("debug/E.ssv", 'a+') as efile:
				efile.write(SEPARATOR.join([uname, het, nap, tant, anyag]) + '\n')
		if het == "J":
			with open("debug/J.ssv", "a+") as jfile:
				jfile.write(SEPARATOR.join([uname, het, nap, tant, anyag]) + '\n')

		return Response(json.dumps('SUCCESS'), mimetype='application/json')

if __name__ == '__main__':
	filetrunc();
	app.run()
