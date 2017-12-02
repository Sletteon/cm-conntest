<!Doctype html>
<b>Szerver-kliens kapcsolatteszt</b><br>
[![Build Status](https://travis-ci.org/Sletteon/cm-conntest.svg?branch=master)](https://travis-ci.org/Sletteon/cm-conntest)
<h3>Hasznos linkek</h3>
<a href = "http://docs.phonegap.com/">PhoneGap dokumentáció</a><br>
<a href="https://cordova.apache.org/docs/en/latest/">Cordova dokumentáció</a><br>
<a href = "https://build.phonegap.com/apps/2893794/download/android/?qr_key=a5nry2YDex911S8dvqJu">Legstabilabb apk</a><br>
<b>Szerver:</b><br>
A szerver mappában 3 fájl található; egy server.py, libserver.py és az ex[tended]libserver.py.<br>
A server.py-t kell futtatni, hogy elinduljon a szerver.<br>
A serverlib-ben lévő PyWSock osztályt kiegészíti a PyWSockFunc (exlibserver.py) ostály, amiben a handle_clients methóduson kívűl minden egyéb funkciót tárolunk.<br>
A szerver nem csak LAN hálózatokon működik.<br>
A szerver egyenlőre elfogadja a kliens csatlakozását, handshake történik, amit a kliens által megadott szövegek kiírása követ.<br>
Egy csatlakozásnál csak egyszer fogadhat adatot a szerver, így ezt kicselezve, majd minden rögzített változásnál egy új kapcsolat jön létre.<br>
Ez még azért is jó, mert így lehetséges lesz az offline munka.<br>
A szerver elmenti, amit kapott set parancsokat, és egy get paranccsal elérhető ez a lista.<br>
Példa a set parancsra:

```
misi;set;E;H;töri;frank birodalom;
```

Ahol misi a felhasználónév, amit első indításnál elkér a weboldal,
[E]z a hét [H]étfőjére töriből a frank birodalom lesz a tananyag.<br>
Példa a get parancsra:

```
misi;get;E;
```

Ahol a misi felhasználó [E]rre a hétre akar készülni.<br>

Napok: [H]étfő | [K]edd | [S]zerda | [C]sütörtök | [P]éntek<br>
Hetek: [E]z a hét [J]övő hét<br>

<b>Kliens:</b><br>
A klienst a Phone Gap programmal, HTML, JS illetve CSS nyelveken írjuk.<br>
A program ezt a weboldalt (index.html) mobil alkalmazásra fogja fordítani <a href = "https://build.phonegap.com">ezen</a> az oldalon.<br>
Debuggolás folyamata a böngészőben történik a fejlesztői eszközök miatt.<br>
index.html helye: /kliens/www/index.html<br>
Ha egy sikeres handshake történik a szerver és a kliens között, megnézi, van-e egy felhasználónév mentve.<br>
Amennyiben nincs, egy gyors promptal bekér egyet és elküldi a szervernek, ha talált, akkor azt a nevet küldi el. <br>
