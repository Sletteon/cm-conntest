**ClassMate, egy mobil app, ahol meg tudod nézni a leckéket, amiket az osztálytársaid küldtek be**<br>

 **Hasznos linkek**<br>
[Legstabilabb kliens (android)](https://build.phonegap.com/apps/2934479/download/android)<br><hr>

**Hogyan futtatsd**<br>

*Kliens*<br>
Én buildelem az appot, így azzal nincs sok teendő.<br>

*Szerver*<br>
FONTOS: ugyanabban a mappában kell lenni, amiben a server.py megtalálható.

Függőségek telepítése:
```# pip3 install -r requirements.txt```

Indítás:
```$ python3 szerver.py ../config/production.ini```

ERRE FIGYELJ:

Néhány Linux rendszeren a 3-s szám elhagyható, csak arra kell ügyelni, hogy a Python 3-s verziójával indítsuk el a szervert.<br>

Ha a MongoDB telepítve van és létre van hozva a `cm` n. adatbázis benne `posts` collection-nel, akkor a production.ini helyett a local.ini fájlt adjuk meg.<br>

Valamiért a Debian virtuális gépemben néha nem szokott válaszolni a szerver, így azt tmux alatt futtatom. Még egy előnye a programnak, hogy amellett, hogy fut a szerver, szerkezteni tudom a modt.txt-t is.<br> 

*autoTestClient.py*<br>
Arra való, hogy a szerver teljesítményét/működését teszteljük.<br>
Függőségek: csak a `requests` Python modul.<br>
Használat: <br>
```$ python3 autoTestClient.py <szerverIP>:<opcionális, szerver port> <opcionális, egy kép útvonala> ```<br>

Megintcsak, Linux disztófüggő, hogy kell-e 3-s a `python3`-ba.<br>

**Fejlesztés**<br>

Mindent a Github Projects fülében dokumentálunk, így mindig tudjuk, hogy a másik (forever alone) min dolgozik.<br>

*Kliens*<br>

A kliens mappája, amin mi, emberek, dolgozunk, nem más, mint, a `kliens/www`.
A többi kliens fájlhoz a PhoneGap szokott hozzányúlni, így én nem is nagyon piszkáltam bele.
Említeni sem érdemes, hogy az index.html a főoldal, azt látja először a kedves felhasználó.<br>

*Szerver*<br>

A szerver mappaszerkezete egyszerűbb, mivel azt csak emberi kézzel építettem. (ezért olyan ronda a kód :joy:)
A debug mappában most már semmit nem tárolunk, csak régebben, amikor fájlokkal szenvedtem, és nem adatbázissal.
A lib mappában a server.py futtatásához szükséges fájlok találhatóak. Feljeszés során itt telik el az idő legtöbb része.
A log fájljainak célja szerintem egyértelmű. Ha a távollétünkben valamilyen hiba történt, akkor vissza lehessen keresni a hiba okát.
testPics mappa csak pár képet tartalmaz, amivel a képbeküldést teszteltem.
Az autoTestClient.py használatát már leírtam, csak úgy, mint a requirements.txt-ét.
motd.txt-be kerülnek a napi üzenetek, míg a szerver.py fájllal indítjuk el a cirkuszt.
