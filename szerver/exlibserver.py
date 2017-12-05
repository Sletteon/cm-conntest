# -*- coding: utf-8 -*-
import socket
import hashlib
import base64
import threading
import time
# =======
# Ez az osztály kiegészíti a PyWSock osztályt ami a libservet.py fileban található
# =======


class PyWSockFunc:
    MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
        "Upgrade: websocket\r\n" + \
        "Connection: Upgrade\r\n" + \
        "Sec-WebSocket-Accept: %s\r\n" + \
        "\r\n"

    def parseHeaders(self, data):
    	headers = {}
    	lines = data.splitlines()
    	for l in lines:
        	parts = l.split(": ", 1)
        	if len(parts) == 2:
				headers[parts[0]] = parts[1]
		headers['code'] = lines[len(lines) - 1]
    	return headers

    # egyrészt a http követeli meg a handshaket, de még a kapcsolat tesztelésére is jó
    def handshake(self, client, addrh):
        # print('<-> Handshake: ' + addrh[0])
        data = client.recv(2048)
        headers = self.parseHeaders(data)
        # print('<+> Handshake sikeres')
        key = headers['Sec-WebSocket-Key']
        responseData = self.HSHAKE_RESP % (
            (base64.b64encode(hashlib.sha1(key + self.MAGIC).digest()),))
        #print('[%s]' % (responseData,))
        return client.send(responseData)

    def receiveData(self, client):
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
        dataString = ''
        if(datalen > 0):
            maskKey = data[2:6]
            maskedData = data[6:(6 + datalen)]
            unmaskedData = [maskedData[i] ^ maskKey[i % 4]
                            for i in range(len(maskedData))]
            dataString = str(bytearray(unmaskedData))
        return dataString

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

    # listát sztringekbe konvertálja, és így olvassa be a klienseknek
    def szepitveBeolvas(self, xfiletart):
        # létrehoz egy stringet az xfiletart listábol
        xfiletartstr = "".join(str(x) for x in xfiletart)
        # ha szóköz nélküli adat nem üres, küldje azt el
        if xfiletartstr.replace(" ", "") != "":
            self.broadcast(xfiletartstr)
            # egyébként sokszor utálom, de most jól jön
            # egy üres line ez a print után,
            # ugyanis mi hármasával küldjük el az xfiletartstr-t,
            # és nagyon szépen elválasztja 3-asával a küldött parancsokat
            print(xfiletartstr)

    # csak elmenti a megadott fájlba a megadott adatot,
    # mivel kétszer kellett ugyanazt írnom, gondoltam,
    # talán egyszerübben fut, ha külön metódusba írom
    def ment(self, xfile, data):
		xfile.write(data + '\n')
		xfile.close()

    # fájlok tartalmának törlése, ha nincs meg a fájl,
    # hozza létre azt.
    # Ha felhasználóknak adjuk, TÖRÖLNI kell
    # ha mégse, a beírt parancsok csak a szerver futásáig
    # maradnak meg
    def filetrunc(self):
        efile = open("debug/E.ssv", "a+")
        efile.truncate()
        efile.close()

        jfile = open("debug/J.ssv", "a+")
        jfile.truncate()
        jfile.close()

    # 3-asával elküldi a parancsokat (szépítve)
    def listatKuld(self, lista):
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
