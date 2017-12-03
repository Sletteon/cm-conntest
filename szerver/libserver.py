# -*- coding: utf-8 -*-
# importok
import threading, time, socket
from exlibserver import PyWSockFunc
# hatalmas segítség: https://stackoverflow.com/questions/18240358/html5-websocket-connecting-to-python

# Jelek:
#     <+> : Rendben lezajlott a megadott funkció/parancs
#     <-> : Semmi extra
#     <!> : Kisebb hiba (csak 1 szál áll le, ami újraindul)
#     <<!>> : Végzetes hiba
#     ++++<IP-cím>++++ : IP-című kliens csatlakozott
#     ----<IP-cím>---- : IP-című kliens lekapcsolódott

# =====================================
# ELIGAZODÁS:
# 		A szerver.pyban meghívjuk egy objekummal a PyWSock osztálynak
#		a __init__ metódusát.
# 		Ez a metódus a beérkező kapcsolatokat fogadja el,
# 		minden kliensnek fusson le a handle_client, külön-külön szálakon.
# 		Az exlibserver.py fájlban a klienseknek futásához szükséges
#		globális változókat, illetve további metódusokat találjuk meg, amik
# 		többnyire a handle_client funkcióban kerülnek felhasználásra,
# 		illetve meghívásra.
# 		A szervert tehát 2 while(True) ciklus hajtja: egy figyelő, illetve egy
# 		kliens-kiszolgáló.
# 		Az utóbbiban a loop a kliensek parancsat figyeli, illetve azokra reagál.
# =====================================

class PyWSock(PyWSockFunc):
	LOCK = threading.Lock()
	# kliens lista deklarálása
	clients = []

	# mindent elindít
	def __init__(self, port):
		self.filetrunc()
		# socket cuccok
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('', port))
		# maximum 50 kapcsolatot fogadjon el
		# lehetne sokkal kevesebb is, mert a kapcsolat nem keep-alive,
		# a kliensek kevés idő erejéig kapcsolódnak a szerverhez,
		# legalábbis ezt tervezem
		s.listen(50)
		print ('<+> Szerver online')
		while(1):
			# fogadjon el minden beérkező kapcsolatot
			conn, addr = s.accept()
			# írja ki szépen a kliensek IP-címét,
			# jó sok plusszal, hogy látszódjon, ki kapcsolódott
			print ('+++' + addr[0] + '+++')
			# threadingesen hívja meg a handle_client metódust
			# gondolom külön-külön szálakat foglaljon le a handle_client metódusnak
			threading.Thread(target = self.handle_client, args = (conn, addr)).start()
			# threading cuccok, kliensek objektumát írja a
			# kliens lista végére.
			self.LOCK.acquire()
			self.clients.append(conn)
			self.LOCK.release()
			time.sleep(0.1)

	# mit csináljon a kliensekkel (egyenként)
	def handle_client (self, client, addr):
		# handshake
		self.handshake(client, addr)
		# nyissa meg az E.db fájlt, írás-olvasás joggal
		efile = open("debug/E.ssv","a+")
		jfile = open("debug/J.ssv","a+")

		try:
			while 1:
				# Adat elkapása
				data = self.recv_data(client)
				print("Parancs: " + data)

				# hozza létre az efiletart változót,
				# és mindig frissítse, így mindenki a legfrissebb
				# változatot kapja
				# efiletart: [e]z a hét [file]-jának [tart]alma
				efiletart = efile.readlines()
				jfiletart = jfile.readlines()

				# a parancsok stringek, pontosvesszővel elválasztva,
				# itt kerülnek szétbontásra, egy splitdata listába
				splitdata = data.split(';')
				# mindig írja ki a kapott adattól, kitől kaptuk azt
				print ('Felhasználónév: ' + splitdata[0])

				# ha valaki küldött egy set parancsot
				if splitdata[1] == 'set':

					print("Beállítás")

					if splitdata[2] == 'E':
						self.ment(efile, data)
					else:
						if splitdata[2] == 'J':
						   self.ment(jfile, data)

					print ('Nap: ' + splitdata[3])
					print ('Tantárgy: ' + splitdata[4])
					print ('Anyag: ' + splitdata[5])

				else:
					print("Lekérés")
					# ha valaki le szeretné kérni ennek a hétnek az anyagát, küldje is el
					if splitdata[2] == 'E':
						print('Hét: Ez a hét')
						self.listaTobbreOsztvaElkuld(efiletart)
					# jövő hét anyaga, ugyanaz, mint az e heti
					if splitdata[2] == 'J':
						print('Hét: Jövő hét')
						self.listaTobbreOsztvaElkuld(jfiletart)
				# szabályszerűen zárja le a fáljt
				efile.close()
				# ne egye meg a CPU-t
				time.sleep(0.1)

		except Exception as e:
			# ha valami hiba történt, írja ki
			# debughoz hasznos, de gyakran kiírja,
			# hogy adatolvasási hiba
			# és mindig beilleszt egy kéretlen newlinet,
			# hacsak nem ír ki valamit
			print(e)
			# ha nem írunk ki semmit, ne történjen semmi
			# ha tényleg nincs szükségünk az elöbbi printre,
			# ki lehet a try-t törölni
			pass
		# mindenesetben, ha kiléptünk a while loopból,
		# 100% hogy egy kliens lecsatlakozott, írja ki, hogy ki
		print ('---' + addr[0] + '---\n')
		# threading, amihez megint csak keveset értek
		self.LOCK.acquire()
		self.clients.remove(client)
		self.LOCK.release()
		client.close()
