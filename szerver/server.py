# -*- coding: utf-8 -*-
from libserver import PyWSock
import sys
try:
	port = 5000
	if len(sys.argv) == 1:
		print("Port: 5000")
	if len(sys.argv) == 2:
		port = int(sys.argv[1])
	ws = PyWSock(port)
except KeyboardInterrupt:
	exit()
