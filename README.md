**Szerver-kliens kapcsolatteszt**<br>
[![Build Status](https://travis-ci.org/Sletteon/cm-conntest.svg?branch=master)](https://travis-ci.org/Sletteon/cm-conntest)<br>
_A Travis a szervert teszteli, hogy nincs-e szintaxis hiba. A szerver.py minden osztályt meghív, tehát azok <br>
beolvasásakor kiderül, elrontottam-e valamit. (tudom, nincs sok értelme, mert én is lefuttatom a kódot, <br>
de nemrég fedeztem ezt fel, és nagyon tetszik)_<br><br>
**Hasznos linkek**<br>
[PhoneGap dokumentáció](http://docs.phonegap.com/)<br>
[Cordova dokumentáció](https://cordova.apache.org/docs/en/latest/)<br>
[Legstabilabb kliens apk](https://build.phonegap.com/apps/2893794/download/android/?qr_key=a5nry2YDex911S8dvqJu)<br>
**Szerver:**<br>
A szerver mappában 3 fájl található; egy server.py, libserver.py és az ex[tending]libserver.py.<br>
A server.py-t kell futtatni, hogy elinduljon a szerver.<br>
A serverlib-ben lévő PyWSock osztályt kiegészíti a PyWSockFunc (exlibserver.py) osztály, amiben a handle_clients methóduson kívül minden egyéb funkciót tárolunk.<br>
A szerver nem csak LAN hálózatokon működik.<br>
A szerver egyenlőre elfogadja a kliens csatlakozását, handshake történik, amit a kliens által megadott szövegek kiírása követ.<br>
Egy csatlakozásnál csak egyszer fogadhat adatot a szerver, így ezt kicselezve, majd minden rögzített változásnál egy új kapcsolat jön létre.<br>
Ez még azért is jó, mert így lehetséges lesz az offline munka.<br>
A szerver elmenti, amit kapott set parancsokat, és egy get paranccsal elérhető ez a lista.<br>
Példa a set parancsra:

```
misi;set;E;H;töri;frank birodalom;
```

Ahol misi a felhasználónév, amit első indításnál elkér a weboldal, [E]z a hét [H]étfőjére töriből a frank birodalom lesz a tananyag.<br>
Példa a get parancsra:

```
misi;get;E;
```

Ahol a misi felhasználó [E]rre a hétre akar készülni.<br>

Napok: [H]étfő | [K]edd | [S]zerda | [C]sütörtök | [P]éntek<br>
Hetek: [E]z a hét [J]övő hét<br>

**Kliens:**<br>
A klienst a PhoneGap programmal, HTML, JS illetve CSS nyelveken írjuk.<br>
A program ezt a weboldalt (index.html) mobil alkalmazásra fogja fordítani [ezen](https://build.phonegap.com) az oldalon.<br>
Debu ggolás folyamata a böngészőben történik a fejlesztői eszközök miatt.<br>
index.html helye: /kliens/www/index.html<br>
Ha egy sikeres handshake történik a szerver és a kliens között, megnézi, van-e egy felhasználónév mentve.<br>
Amennyiben nincs, egy gyors prompttal bekér egyet és elküldi a szervernek, ha talált, akkor azt a nevet küldi el.<br>
