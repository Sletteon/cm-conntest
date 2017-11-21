# -*- coding: utf-8 -*-
# importok
import socket, hashlib, base64, threading, sys, time
# hasznos cumó: https://stackoverflow.com/questions/18240358/html5-websocket-connecting-to-python

# Használat:
#     Indítás:
#     ws = PyWSock() # objektum létrehozása ws néven
#     ws.start_server(int(sys.argv[1])) # szerver indítása, port az legyen az első flag python <ezafájl.py> <portszám>
#
#     Adatok fogadása:
#     ws.recv_data(<kliensek>)
#     
#     Adatok kiíratása (broadcast):
#     ws.broadcast_resp("valami") # "valami" elküldése mindenkinek
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

    # adatok befogadásához egy methódus
    def recv_data (self, client):

        # a networking legfélelmetesebb része, ezt én egy picit sem értem
        # ez akadályoz meg minket, hogy interaktív kommunikációt folytassunk


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
    def broadcast_resp(self, data):
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
            except:
                print("<!> Broadcast hiba")
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
        self.handshake(client, addr)
        try:
            while 1:            
                # Adat elkapása
                data = self.recv_data(client)
                print("Parancs: %s" % (data,))
                self.broadcast_resp(data)
                splitdata = data.split(';')
                print ('Felhasználónév: ' + splitdata[0])
                if splitdata[1] == 'E':
                    print ('Hét: Ez a hét')
                if splitdata[1] == 'J':
                    print ('Hét: Jövő hét')
                print ('Nap: ' + splitdata[2])
                print ('Tantárgy: ' + splitdata[3])
                print ('Anyag: ' + splitdata[4])
                time.sleep(0.1)
        except:
            pass
        # print('{-} Kliens lekapcsolódott: ' + addr[0])
        print ('======')
        self.LOCK.acquire()
        self.clients.remove(client)
        self.LOCK.release()
        client.close()

    def start_server (self, port):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(50)
        print ('<+> Szerver online')
        while(1):
            conn, addr = s.accept()
            # print ('{+} Kliens csatlakozott: ' + addr[0])
            print ('===' + addr[0] + '===')
            threading.Thread(target = self.handle_client, args = (conn, addr)).start()
            self.LOCK.acquire()
            self.clients.append(conn)
            self.LOCK.release()
            time.sleep(0.1)
