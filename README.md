**Szerver-kliens kapcsolatteszt**<br>
<!-- [![Build Status](http://46.139.116.9:9000/buildStatus/icon?job=cm-conntest)](http://46.139.116.9:9000/job/cm-conntest) -->

<!-- *Jenkins a szerver/autoTestClient.py-t futtatja, ami a mindig elérhető tesztszervert (raspberry pi) teszteli. A teszt 1000 beírásból (teszt száma sha1, és md5 hashben), és egy lekérésből áll.* -->

 **Hasznos linkek**<br>
[PhoneGap dokumentáció](http://docs.phonegap.com/)<br>
[Cordova dokumentáció](https://cordova.apache.org/docs/en/latest/)<br>
[Legstabilabb kliens apk](https://build.phonegap.com/apps/2934479/download/android)<br><hr>
**Függőségek:**

flask, flask_cors, colorama, pymongo, (teszthez) requests<br><br>
**Szerver:**

Amikor a szerverre csatlakozik valaki, megnézi, amennyiben GET eljárást használ a kliens, valószínűleg le szeretné kérni az elmentett adatokat, így azokat JSON formátumban elküldi a szerver. Ha viszont a kliens küldi el az adatokat, azt a szervernek POST metódusával teszi, szintén JSON-ban.

Példa az anyagbeállításra:

_Utf-8-as karakterkódolást a HTML megoldja_

```
[{
    "_id": {
        "$oid": "5a79f0329805160771b1bbe7"
    },
    "uname": "misiCHR",
    "het": 6,
    "nap": "K",
    "tant": "t\u00f6ri",
    "anyag": "frankreichische Reich"
}, {
    "_id": {
        "$oid": "5a79f0449805160771b1bbea"
    },
    "uname": "misiCHR",
    "het": 6,
    "nap": "K",
    "tant": "matek",
    "anyag": "trigonometrie"
}]
```



Jelen esetünkben 2 bejegyzést tárolunk el, ahol a misiCHR nevű felhasználó töriből, illetve matekból írt be [K]eddre, a 6\. hétre.

Napok: [H]étfő | [K]edd | [S]zerda | [C]sütörtök | [P]éntek<br>

**Szerver admin-parancsok:**

Shell-hozzáférés nélkül lehet a szerveren bizonyos funkciókat végrehajtani, debuggolást könnyítve. (lista bővűl)
Használat: tantárgy helyében kell ezeket a parancsokat beírni.

* \* - eddigi adatokat törli ki (csak a teszt-szerveren lesz elérhető)

<hr>

**Kliens:**

A klienst a PhoneGap programmal, HTML, JS illetve CSS nyelveken írjuk.
A program ezt a weboldalt (index.html) mobil alkalmazásra fogja fordítani [ezen](https://build.phonegap.com) az oldalon.
Debuggolás folyamata a böngészőben történik a fejlesztői eszközök miatt.
index.html helye: /kliens/www/index.html
A felhasználó be tud adni adatot, le tud kérni adatot, mindezeket külön gombokkal.
Valamint a gombok alatt, egy link, megnyomása a felhasználónév törlésével, illetve a weboldal újratöltésével jár.
