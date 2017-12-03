#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libserver import PyWSock
from exlibserver import PyWSockFunc
import sys
try:
	port = 5000
	if len(sys.argv) == 1:
		print("Port: 5000")
	if len(sys.argv) == 2:
		if sys.argv[1] == "travis":
			print("<+> Minden jónak tűnik az osztályok felől...")
			exit()
		port = int(sys.argv[1])
	ws = PyWSock(port)
except KeyboardInterrupt:
	exit()
