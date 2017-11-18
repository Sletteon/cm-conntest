<!Doctype html>
#conntest
<b>Szerver-kliens kapcsolatteszt</b><br>
<b>Szerver:</b><br>
A szerver mappában 2 futtatható fájl található; egy server.py és a serverlib.py.<br>
A server.py-t kell futtatni, hogy elinduljon a szerver.<br>
Használat:  
```
python server.py <port száma>
 ```
A szerver nem csak LAN hálózatokon működik.<br>
A szerver egyenlőre elfogadja a kliens csatlakozását, handshake történik, amit a kliens nevének kiírása követ.<br>
Egy csatlakozásnál csak egyszer fogadhat adatot a szerver, így ezt kicselezve, majd minden rögzített változásnál egy új kapcsolat jön létre.<br>
Ez még azért is jó, mert így lehetséges lesz az offline munka.<br>
<b>Kliens:</b><br>
A klienst a Phone Gap programmal, HTML, JS illetve CSS nyelveken írjuk.<br>
A program ezt a weboldalt (index.html) mobil alkalmazásra fogja fordítani <a href = "https://build.phonegap.com">ezen az oldalon.</a><br>
Debuggolás folyamata a böngészőben történik a fejleszői eszközök miatt.<br>
index.html helye: /kliens/www/index.html<br>
A kliens beolvassa a felhasználó által megadott IP-címet, portszámot.<br>
Ha egy sikeres handshake történik a szerver és a kliens között, megnézi, van-e egy felhasználónév mentve.<br>
Amennyiben nincs, egy gyors promptal bekér egyet és elküldi a szervernek, ha talált, akkor azt a nevet küldi el. <br>
