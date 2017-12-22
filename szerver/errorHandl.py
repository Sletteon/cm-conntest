# -*- coding: utf-8 -*-

# Később nem fogja kiírni a hibát, hanem egy logfile-ba jegyzi be
import traceback
from colorPrint import colorPrint

class errorHandl:
	# Fancy módon írja ki, hogy mi a hiba
	# Megjegyzés: azért traceback, mert az megmutatja a sorszámot,
	# ahol a hiba keletkezett
	def errorHandling(self, clientIP):
		printObj = colorPrint()
		printObj.errPrint('Hiba történt egy kliensnél (%s):\n---------------traceback---------------' %(clientIP))
		print(traceback.format_exc())
		print('---------------traceback---------------')
