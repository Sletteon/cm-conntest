# -*- coding: utf-8 -*-
from colorama import Fore, Style

class colorPrint:
	def errPrint(self, message, whiteMessage = ''):
		print(Fore.RED + message + Style.RESET_ALL + whiteMessage)

	def warnPrint(self, message, whiteMessage = ''):
		print(Fore.YELLOW + message + Style.RESET_ALL + whiteMessage)

	def okPrint(self, message, whiteMessage = ''):
		print(Fore.GREEN + message + Style.RESET_ALL + whiteMessage)
