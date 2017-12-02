# -*- coding: utf-8 -*-
from libserver import PyWSock
import sys, time
try:
	port = 5000
	if len(sys.argv) == 1:
		print("Port: 5000")
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	ws = PyWSock()
	ws.start_server(port)
except KeyboardInterrupt:
	exit()
