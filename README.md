**Szerver-kliens kapcsolatteszt**<br>
**Hasznos linkek**<br>
[PhoneGap dokumentáció](http://docs.phonegap.com/)<br>
[Cordova dokumentáció](https://cordova.apache.org/docs/en/latest/)<br>
[Legstabilabb kliens apk](https://build.phonegap.com/apps/2893794/download/android/?qr_key=a5nry2YDex911S8dvqJu)<br>
**Függőségek:**<br>
flask, flask_cors<br>
**Szerver:**<br>
Egy csatlakozásnál csak egyszer fogadhat adatot a szerver, így ezt kicselezve, majd minden rögzített változásnál egy új kapcsolat jön létre.<br>
Ez még azért is jó, mert így lehetséges lesz az offline munka.<br>
A szerver elmenti, amit kapott set parancsokat, és egy get paranccsal elérhető ez a lista.<br>
Példa a set parancsra:<br>

```
misi<|>set<|>E<|>H<|>töri<|>frank birodalom<|>
```

_Adatok elválasztásához a következő szöveget használjuk: <|>_<br>
_Elég kicsi a valószínűsége annak, hogy ezt a karaktersort valaki beírná (főleg mobilon)_

Ahol misi a felhasználónév, amit első indításnál elkér a weboldal, [E]z a hét [H]étfőjére töriből a frank birodalom lesz a tananyag.<br>
Példa a get parancsra:

```
misi<|>get<|>E<|>
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
