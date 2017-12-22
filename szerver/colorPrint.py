# -*- coding: utf-8 -*-


from colorama import Fore, Style

class colorPrint:
	def errPrint(self, message):
		print('\n' + Fore.RED + '[&&&] ' + Style.RESET_ALL + message)

	def warnPrint(self, message):
		print('\n' + Fore.YELLOW + '[*] ' + Style.RESET_ALL + message)

	def okPrint(self, message):
		print('\n' + Fore.GREEN + '[+] ' + Style.RESET_ALL + message)

	def finePrint(self, message):
		print('\n' + Fore.CYAN + '[-] ' + Style.RESET_ALL + message)
