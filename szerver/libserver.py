# -*- coding: utf-8 -*-
# importok
import socket, hashlib, base64, threading, sys, time
# hasznos cumó: https://stackoverflow.com/questions/18240358/html5-websocket-connecting-to-python

# Használat:
#     #Indítás:
#     ws = PyWSock() # objektum létrehozása ws néven
#     ws.start_server(int(sys.argv[1])) # szerver indítása, port az legyen az első flag python <ezafájl.py> <portszám>
#
#     #Adatok fogadása:
#     ws.recv_data(<kliensek>)
#     
#     #Adatok kiíratása mindenkivel(broadcast):
#     ws.broadcast("valami") # "valami" elküldése mindenkinek
#
# Jelek:
#     <+> : Rendben lezajlott a megadott funkció/parancs
#     <-> : Semmi extra
#     <!> : Kisebb hiba (csak 1 szál áll le, ami újraindul)
#     <<!>> : Végzetes hiba

class PyWSock:
    MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    # ha rossz a handshake válasz, nem működik a kapcsolat,
    # nem kéne ezt megváltoztatni, mert eleve elég átláthatatlan
    HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
                "Upgrade: websocket\r\n" + \
                "Connection: Upgrade\r\n" + \
                "Sec-WebSocket-Accept: %s\r\n" + \
                "\r\n"

    LOCK = threading.Lock()

    # kliens lista deklarálása
    clients = []

    # adatok befogadásához egy metódus
    def recv_data (self, client):

        # a networking legfélelmetesebb része, ezt én egy picit sem értem
        # ez akadályoz meg minket, hogy interaktív kommunikációt folytassunk,
        # de én nem is sajnálom


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
    
    # formázás
    def parse_headers (self, data):
        headers = {}
        lines = data.splitlines()
        for l in lines:
            parts = l.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]
        return headers

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

                # ha kapott egy parancsot, elsősorban írja ki azt
                # nem szükséges, talán hátráltathat is.
                # ki kéne törölni
                #self.broadcast(data)
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
                        if len(efiletart) >= 3:
                            listOfEfiletart = self.listaszaggato(efiletart)
                            x = 0
                            y = 3
                            self.szepitveBeolvas(efiletart[x:y])
                            for i in range(len(efiletart) - 3):
                                x += 3
                                y += 3
                                self.szepitveBeolvas(efiletart[x:y])
                        if len(efiletart) == 1:
                            self.szepitveBeolvas(efiletart)

                        #self.listaKetteosztvaElkuld(efiletart, 0, 3)
                        #self.listaKetteosztvaElkuld(efiletart, 4, 7)

                    # jövő hét anyaga, ugyanaz, mint az e heti
                    if splitdata[2] == 'J':
                        print('Hét: Jövő hét')
                        self.szepitveBeolvas(jfiletart)
                # szabályszerűen zárja le a fáljt
                efile.close()
                # ne egye meg a CPU-t
                time.sleep(0.1)

        except Exception as e:
            # ha valami hiba történt, írja ki
            # debughoz hasznos, de gyakran kiírja, 
            # hogy adatolvasási hiba,
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
    
    # listát sztringekbe konvertálja, és így olvassa be a klienseknek
    def szepitveBeolvas(self, xfiletart):
        xfiletartstr = "".join(str(x) for x in xfiletart)

        if xfiletartstr.replace(" ","") == "":
            pass
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

    def listaszaggato(self, x):
        return [x[i:i+3] for i in range(0, len(x), 3)]

    def listaKetteosztvaElkuld(self, lista,  minLength, maxLength):
        if len(lista) >= minLength and len(lista) <= maxLength:
            self.szepitveBeolvas(lista[minLength:maxLength])
                                    

    def start_server (self, port):
        self.filetrunc()
        # socket cuccok
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        # maximum 50 kapcsolatot fogadjon el
        # lehetne sokkal kevesebb is, mert a kapcsolat nem keep-alive,
        # a kliensek kevés idő erejéig kapcsolódnak a szerverhez
        s.listen(50)
        print ('<+> Szerver online')
        while(1):
            # fogadjon el minden beérkező kapcsolatot
            conn, addr = s.accept()
            # írja ki szépen a kliensek IP-címét, 
            # jó sok plusszal, hogy látszódjon, ki kapcsolódott
            print ('+++' + addr[0] + '+++')
            threading.Thread(target = self.handle_client, args = (conn, addr)).start()
            # threading cuccok, kliensek objektumát írja a 
            # kliens lista végére.
            self.LOCK.acquire()
            self.clients.append(conn)
            self.LOCK.release()
            time.sleep(0.1)
