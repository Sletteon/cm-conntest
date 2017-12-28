# -*- coding: utf-8 -*-

# Színesen kiírja az állapotnak megfelelő ikont, és utána a szöveget
from colorama import Fore, Style

class colorPrint:
	def errPrint(self, message):
		print('\n' + Fore.RED + '[&&&] ' + Style.RESET_ALL + message)

	def warnPrint(self, message):
		print('\n' + Fore.YELLOW + '[*] ' + Style.RESET_ALL + message)

	def okPrint(self, message):
		print('\n' + Fore.GREEN + '[+] ' + Style.RESET_ALL + message)

	def finePrint(self, message):
		print('\n' + Fore.BLUE + '[-] ' + Style.RESET_ALL + message)
