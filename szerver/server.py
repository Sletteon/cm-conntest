# -*- coding: utf-8 -*-
import os
import logging
import socket
from flask import Flask, request, Response, json
from flask_cors import CORS

# Ne látszódjanak a werkzeug (többek között HTTP-log) cuccai
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__, static_folder=os.path.join(os.environ['PWD'], 'client'))
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})

# Törölje a megnyitott fájlok tartalmát
def filetrunc():
    with open('debug/data.json', 'w', encoding='utf-8') as efile:
        efile.truncate()
        efile.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Csatlakozott kliens IP-címe
    clientIP = request.remote_addr

    if request.method == 'POST':
        gotJSON = request.get_json()
        # [*] jancsi (jancsi.ip.címe.briós) bejegyzése:
        print('\n' + '[*] ' + str(gotJSON['uname']) +
              ' (' + clientIP + ') ' + 'bejegyzése: ')

        try:
            # Adatok kiírása
            print('--- Hét: ' + str(gotJSON['het']))
            print('--- Nap: ' + str(gotJSON['nap']))
            print('--- Tantárgy: ' + str(gotJSON['tant']))
            print('--- Anyag: ' + str(gotJSON['anyag']))

            # Adatok mentése
            with open('debug/data.json', 'a', encoding='utf-8') as file:
                json.dump(gotJSON, file, ensure_ascii=False)
                file.write('\n')

        except KeyError:
            return Response(json.dumps({'ERROR': 'JSON ERROR'}), status=422, mimetype='application/json')

        return Response(json.dumps('SUCCESS'), mimetype='application/json')
    else:  # request.method == 'GET'
        # [*] Hétlekérés: jancsi.ip.címe.túróstáska
        print('\n' + '[*] Anyaglekérés: ' + clientIP)

        # Nyissa meg a fájlt, tartalmát küldje el
        with open('debug/data.json', 'r', encoding='utf-8') as file:
            #fileList = file.readlines()
            return Response("\n".join(file.readlines()))


if __name__ == '__main__':
    # Ha bennhagyjuk, a rögzített bejegyzések úrjaindításkor törlődnek
    filetrunc()

    # Pozitívum, ha már itt tartunk
    # Lokális IP-cím lekérése zajlik a 'szerver fut' felirat mellett.
    print('[+] Szerver fut: ' + (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
                                  or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
    app.run(host='0.0.0.0')
