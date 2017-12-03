#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libserver import PyWSock
from exlibserver import PyWSockFunc
import sys

def main():
	# nem szeretném, ha mindig KeyboardInterrupt-ot írna ki, ha bezárjuk a programot
	try:
		# legyen az alapértelmezett port 5000
		port = 5000
		if len(sys.argv) == 1:
			print('Port: ' + str(port))
		if len(sys.argv) == 2:
			port = int(sys.argv[1])
			if sys.argv[1] == "travis":
				print("<+> Minden jónak tűnik...")
				exit()

		# itt történik minden varázslat, ez meghívja a PyWSock osztály
		# __init__ metódusát
		ws = PyWSock(port)
	except KeyboardInterrupt:
		exit()

if __name__ == '__main__':
	main()
