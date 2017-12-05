# -*- coding: utf-8 -*-
# importok
import threading
import time
import socket
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
# 		minden kliensnek fusson le a handleClient, külön-külön szálakon.
# 		Az exlibserver.py fájlban a klienseknek futásához szükséges
#		globális változókat, illetve további metódusokat találjuk meg, amik
# 		többnyire a handleClient funkcióban kerülnek felhasználásra,
# 		illetve meghívásra.
# 		A szervert tehát 2 while(True) ciklus hajtja: egy figyelő, illetve egy
# 		kliens-kiszolgáló.
# 		Az utóbbiban a loop a kliensek parancsat figyeli, illetve azokra reagál.
# =====================================


class PyWSock(PyWSockFunc):
    LOCK = threading.Lock()
    clients = []

    def __init__(self, port):
        self.filetrunc()
        # socket cuccok
        socketObj = socket.socket()
        socketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketObj.bind(('', port))
        # maximum 50 kapcsolatot fogadjon el
        # lehetne sokkal kevesebb is, mert a kapcsolat nem keep-alive,
        # a kliensek kevés idő erejéig kapcsolódnak a szerverhez,
        # legalábbis ezt tervezem
        socketObj.listen(50)
        print('<+> Szerver online')
        while 1:
            conn, addr = socketObj.accept()
            # írja ki szépen a kliensek IP-címét,
            # jó sok plusszal, hogy látszódjon, ki kapcsolódott
            print('+++' + addr[0] + '+++')
            # threadingesen hívja meg a handleClient metódust
            # gondolom külön-külön szálakat foglaljon le a handleClient metódusnak
            threading.Thread(target=self.handleClient,
                             args=(conn, addr)).start()
            # threading cuccok, kliensek objektumát írja a
            # kliens lista végére.
            self.LOCK.acquire()
            self.clients.append(conn)
            self.LOCK.release()
            time.sleep(0.1)

    # mit csináljon a kliensekkel (egyenként)
    def handleClient(self, client, addr):
        self.handshake(client, addr)
        # nyissa meg a fájlokat, írás-olvasás joggal
        EFile = open("debug/E.ssv", "a+")
        JFile = open("debug/J.ssv", "a+")

        try:
            while 1:
                # Adat elkapása
                data = self.receiveData(client)
                print("Parancs: " + data)

                # hozza létre az EFileTart változót,
                # és mindig frissítse, így mindenki a legfrissebb
                # változatot kapja
                # EFileTart: [e]z a hét [file]-jának [tart]alma
                EFileTart = EFile.readlines()
                JFileTart = JFile.readlines()

                splitdata = data.split('<|>')
                print('Felhasználónév: ' + splitdata[0])

                if splitdata[1] == 'set':

                    print("Beállítás")

                    if splitdata[2] == 'E':
                        self.ment(EFile, data)
                    else:
                        if splitdata[2] == 'J':
                            self.ment(JFile, data)

                    print('Nap: ' + splitdata[3])
                    print('Tantárgy: ' + splitdata[4])
                    print('Anyag: ' + splitdata[5])

                else:
                    print("Lekérés")
                    if splitdata[2] == 'E':
                        print('Hét: Ez a hét')
                        self.listatKuld(EFileTart)
                        EFile.close()
                    if splitdata[2] == 'J':
                        print('Hét: Jövő hét')
                        self.listatKuld(JFileTart)
                        JFile.close()
                # ne egye meg a CPU-t
                time.sleep(0.1)

        except Exception as error:
            # ha valami hiba történt, írja ki
            # debughoz hasznos, de gyakran kiírja,
            # hogy adatolvasási hiba
            # és mindig beilleszt egy kéretlen newlinet,
            # hacsak nem ír ki valamit
            print(error)
            # ha nem írunk ki semmit, ne történjen semmi
            # ha tényleg nincs szükségünk az elöbbi printre,
            # ki lehet a try-t törölni
            pass
        # mindenesetben, ha kiléptünk a while loopból,
        # 100% hogy egy kliens lecsatlakozott
        print('---' + addr[0] + '---\n')
        self.LOCK.acquire()
        self.clients.remove(client)
        self.LOCK.release()
        client.close()
