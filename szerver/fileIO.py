# -*- coding: utf-8 -*-
import json

class fileIO:
	# JSON adatok mentése
	def writeJSONToFile(self, file, JSON):
		with open(file, 'a', encoding='utf-8') as fileobj:
			json.dump(JSON, fileobj, ensure_ascii=False)
			fileobj.write('\n')

	def readJSONFormFile(self, file):
		with open(file, 'r', encoding='utf-8') as file:
			return "\n".join(file.readlines())

	def filetrunc(self):
		with open('debug/data.json', 'w', encoding='utf-8') as file:
			file.truncate()
			file.close()


if __name__ == '__main__':
	print("[!] Nem elindítandó szkript")
