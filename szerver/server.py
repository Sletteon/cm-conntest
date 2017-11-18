# -*- coding: utf-8 -*-
from serverlib import PyWSock
import sys
try:
    if len(sys.argv) != 2:
        print('Használat: python <ez a fájl.py> <portszám>')
        exit()
    ws = PyWSock()
    ws.start_server(int(sys.argv[1]))
except KeyboardInterrupt:
    exit()
