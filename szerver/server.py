#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    ######################################
#    cm-kapcsolatteszt szerveroldali szkript
#
#     Flask ügye, ha ez a gép egy kérést kap, akkor futtassa le az index() függvényt.
#     Amennyiben GET metódussal csatlakoztak kliensek erre a szerverre,
#    lekérnek adatot, így a POST metódussal beküldött adatokat,
#    JSON formában visszaszolgálja.
#    ######################################

# [+] Hiba nélkül történt valami (zöld)
# [-] Semmi extra (kék)
# [*] Nem végzetes hiba (sárga)
# [&&&] Végzetes hiba (piros, alig látszik)

# Standard könyvárak
import os
import logging
import socket
import sys

# Hozzáadott könyvárak
from flask import Flask, request, Response
from flask_cors import CORS

# Saját osztáyok
from lib.reqHandl import *
from lib.colorPrint import *
from lib.errorHandl import *
from lib.config import *

# Ne látszódjanak a werkzeug (többek között HTTP-log) cuccai
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__, static_folder=os.path.join(os.environ['PWD'], 'kliens'))
# Kell, ha nincs akkor kliens hibát kap
CORS(app, resources={r'/*': {'origins': '*'}})


@app.errorhandler(404)
def badRequest(e):
    return Response(RequestError(request, 404), status=404, mimetype='application/json')


@app.errorhandler(400)
def badRequest400(e):
    return Response(RequestError(request, 400, errorCodeToldalek='-as'), status=400, mimetype='application/json')


@app.errorhandler(500)
def badRequest500(e):
    return Response(RequestError(request, 500, errorCodeToldalek='-as'), status=500, mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    """ GET - Minden hét lekérése (nem kéne használni, de még nem törlöm ki)
        POST - Beküldés"""
    # Csatlakozott kliens IP-címe
    clientIP = request.remote_addr
    if request.method == 'POST':
        return onReceivePost(clientIP)
    else:  # request.method == 'GET'
        return onReceiveGet(clientIP)


@app.route('/het/<Het>', methods=['GET'])
def lekeres(Het):
    """ GET - Meghatározott hét lekérése """
    clientIP = request.remote_addr
    return onReceiveSpecifiedGet(clientIP, Het)


@app.route('/getRecord', methods=['GET'])
def adatSzama():
    clientIP = request.remote_addr
    return onReceiveRecordNumberGet(clientIP)

@app.route('/delete/<objectIdToDelete>', methods=['DELETE'])
def megadottBejegyzesTorlese(objectIdToDelete):
    clientIP = request.remote_addr
    return onReceiveDelete(clientIP, objectIdToDelete)


# Lokális Ip-t (hálózaton belülit) ad vissza
# Ha nem vagyunk online, OSError-t dob fel


def getlocalIp():
    return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]


if __name__ == '__main__':
    try:
        config = init_config(sys.argv[1])

        port = int(config['server']['port'])
        
        if port < 1000:
            lowPortNumberWarn()

        localIp = getlocalIp()

    except IndexError:  # nincs port
        try:  # van internet, nincs port
            startPrint(getlocalIp() + ':5000')
            app.run(host='0.0.0.0')
        except OSError:  # nincs internet, nincs port
            startPrintNoIP()
            okPrint('Szerver elérhető az 5000-s porton')
            app.run(host='0.0.0.0')

    except ValueError:  # ha a felhasználó nem érvényes portszámot adott meg
        notValidPortNumberErr()

    except OSError:  # nincs internet, van port
        startPrintNoIP()
        okPrint('Szerver elérhető a %s-s porton' % (str(port)))
        app.run(host='0.0.0.0', port=port)

    else:  # van internet, van port
        startPrint('%s:%s' % (localIp, str(port)))
        app.run(host='0.0.0.0', port=port)
