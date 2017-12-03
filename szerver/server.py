#!/usr/bin/env python
# -*- coding: utf-8 -*-
# importolja az összes osztályt (kivéve modul)
from libserver import PyWSock
from exlibserver import PyWSockFunc
# a sys modul a flagek beolvasásához kell
import sys

def main():
	# nem szeretném, ha mindig KeyboardInterrupt-ot írna ki, ha bezárjuk a programot
	try:
		# legyen az alapértelmezett port 5000
		port = 5000
		# ha csak 1 flaget adtak meg (fájlnév is számít)
		if len(sys.argv) == 1:
			# írja ki a portszámot
			print('Port: ' + port)
		# ha összesen 2 flaget adtak meg
		if len(sys.argv) == 2:
			# ha az extra flag "travis" akkor csak lépjen ki
			if sys.argv[1] == "travis":
				print("<+> Minden jónak tűnik...")
				exit()
			# ha a flag nem travis akkor legyen a portszám a flag
			port = int(sys.argv[1])
			# itt történik minden varázslat, ez meghívja a PyWSock osztály
			# __init__ metódusát
			ws = PyWSock(port)
	except KeyboardInterrupt:
		exit()

# nem kötelező, de én nem bízok ennyire a funkciókon kívüli kódokban (kivéve globális változó)
if __name__ == '__main__':
	main()
