# -*- coding: utf-8 -*-

# Színesen kiírja az állapotnak megfelelő ikont, és utána a szöveget
from colorama import Fore, Style

class colorPrint:
	def errPrint(self, message):
		print('\n' + Fore.RED + Style.BRIGHT + '[&&&] ' + Style.RESET_ALL + message)

	def warnPrint(self, message):
		print('\n' + Fore.YELLOW + Style.BRIGHT + '[*] ' + Style.RESET_ALL + message)

	def okPrint(self, message):
		print('\n' + Fore.GREEN + Style.BRIGHT + '[+] ' + Style.RESET_ALL + message)

	def finePrint(self, message):
		print('\n' + Fore.BLUE + Style.BRIGHT + '[-] ' + Style.RESET_ALL + message)


	def startPrint(self, IpAddress):
		print(Fore.GREEN + Style.BRIGHT + '[+] ' + Style.RESET_ALL + 'Szerver fut: ' + IpAddress)

	def startPrintNoIP(self):
		print(Fore.YELLOW + Style.BRIGHT + '[*] ' + Style.RESET_ALL + 'Szerver fut, de nem lehetett IP-címet megállapítani')

	def lowPortNumberWarn(self):
		print(Fore.YELLOW + Style.BRIGHT + '[*] ' + Style.RESET_ALL + 'Nem javasolt 1000-nél kisebb portszámot megadni\n')

	def notValidPortNumberErr(self):
		print(Fore.RED + Style.BRIGHT + '[&&&] ' + Style.RESET_ALL + 'Portszám csak teljes szám lehet')
