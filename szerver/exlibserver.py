# -*- coding: utf-8 -*-
import socket, hashlib, base64, threading, time
class PyWSockFunc:
	# handshakelés, ne írja ki a választ, csak annyit, hogy sikeres volt-e
	# egyrészt a http követeli meg a handshaket, de még a kapcsolat tesztelésére is jó
	def handshake (self, client, addrh):
		# print('<-> Handshake: ' + addrh[0])
		data = client.recv(2048)
		headers = self.parse_headers(data)
		# print('<+> Handshake sikeres')
		key = headers['Sec-WebSocket-Key']
		resp_data = self.HSHAKE_RESP % ((base64.b64encode(hashlib.sha1(key+self.MAGIC).digest()),))
		#print('[%s]' % (resp_data,))
		return client.send(resp_data)

	# adatok befogadásához egy metódus
	# na ezt a methódust nem értem
	def recv_data (self, client):
		# as a simple server, we expect to receive:
		#    - all data at one go and one frame
		#    - one frame at a time
		#    - text protocol
		#    - no ping pong messages
		data = bytearray(client.recv(512))
		if(len(data) < 6):
			raise Exception("Adatolvasás hiba")
		# FIN bit must be set to indicate end of frame
		assert(0x1 == (0xFF & data[0]) >> 7)
		# data must be a text frame
		# 0x8 (close connection) is handled with assertion failure
		assert(0x1 == (0xF & data[0]))
		# assert that data is masked
		assert(0x1 == (0xFF & data[1]) >> 7)
		datalen = (0x7F & data[1])
		#print("received data len %d" %(datalen,))
		str_data = ''
		if(datalen > 0):
			mask_key = data[2:6]
			masked_data = data[6:(6+datalen)]
			unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
			str_data = str(bytearray(unmasked_data))
		return str_data

		# broadcast = mindenkinek üzenetet kiküldeni
		# lényegében egy tuningolt client.send
	def broadcast(self, data):
		# 1st byte: fin bit set. text frame bits set.
		# 2nd byte: no mask. length set in 1 byte.
		resp = bytearray([0b10000001, len(data)])
		# append the data bytes
		for d in bytearray(data):
			resp.append(d)
		self.LOCK.acquire()
		for client in self.clients:
			try:
				client.send(resp)
			except Exception as e:
				print("<!> Broadcast hiba:" + e)
		self.LOCK.release()

	# formázás (szintén nem értem)
	def parse_headers (self, data):
		headers = {}
		lines = data.splitlines()
		for l in lines:
			parts = l.split(": ", 1)
			if len(parts) == 2:
				headers[parts[0]] = parts[1]
		headers['code'] = lines[len(lines) - 1]
		return headers

	# listát sztringekbe konvertálja, és így olvassa be a klienseknek
	def szepitveBeolvas(self, xfiletart):
		# létrehoz egy stringet az xfiletart listábol
		# ha szóköz nélküli adat nem üres, küldje el
		xfiletartstr = "".join(str(x) for x in xfiletart)
		if xfiletartstr.replace(" ","") != "":
			self.broadcast(xfiletartstr)
			# print('----')
			print(xfiletartstr)
			# print('---')
	# csak elmenti a megadott fájlba a megadott adatot,
	# mivel kétszer kellett ugyanazt írnom, gondoltam,
	# talán egyszerübben fut, ha külön metódusba írom
	def ment(self, xfile, data):
		xfile.write(data + '\n')

	# fájlok tartalmának törlése, ha nincs meg a fájl,
	# hozza létre azt.
	# Ha felhasználóknak adjuk, TÖRÖLNI KELL
	def filetrunc(self):
		efile = open("debug/E.ssv","a+")
		efile.truncate()
		efile.close()

		jfile = open("debug/J.ssv", "a+")
		jfile.truncate()
		jfile.close()

	# 3-asával elküldi a parancsokat (szépítve)
	def listaTobbreOsztvaElkuld(self, lista):
		if len(lista) >= 3:
			x = 0
			y = 3
			self.szepitveBeolvas(lista[x:y])
			for i in range(len(lista) - 3):
				x += 3
				y += 3
				self.szepitveBeolvas(lista[x:y])
			if len(lista) == 1:
				self.szepitveBeolvas(lista)
