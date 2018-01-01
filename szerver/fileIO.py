# -*- coding: utf-8 -*-

# Fájlokkal zsonglőrködik
import json, os

class fileIO:
	scriptPath = os.path.dirname(__file__)
	dataDotJsonPath = os.path.join(scriptPath, 'debug', 'data.json')

	# JSON adatok mentése
	def writeJSONToFile(self, file, JSON):
		with open(file, 'a', encoding='utf-8') as fileobj:
			json.dump(JSON, fileobj, ensure_ascii=False)
			fileobj.write('\n')

	def readJSONFormFile(self, file):
		with open(file, 'r', encoding='utf-8') as file:
			return '\n'.join(file.readlines())

	def filetrunc(self):
		with open(self.dataDotJsonPath, 'w', encoding='utf-8') as file:
			file.truncate()
			file.close()
