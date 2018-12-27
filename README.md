**ClassMate, egy mobil app, ahol meg tudod nézni a leckéket, amiket az osztálytársaid küldtek be**<br>

 **Hasznos linkek**<br>
[Legstabilabb kliens (android)](https://build.phonegap.com/apps/2934479/download/android)<br><hr>
[![Build Status](https://travis-ci.org/Sletteon/cm-conntest.svg?branch=master)](https://travis-ci.org/Sletteon/cm-conntest)

**Hogyan futtatsd**<br>

*Kliens*<br>
Én buildelem az mobil appot, így azzal nincs sok teendő.<br>

*Szerver*<br>

Függőségek telepítése:
```# pip3 install -r requirements.txt```

Indítás:
```$ python3 manage.py runserver```

Első indítás elött:
```$ python3 manage.py migrate```


*autoTestClient.py*<br>
Arra való, hogy a szerver teljesítményét/működését teszteljük.<br>
Használat: <br>
```$ python3 autoTestClient.py <szerverIP>:<opcionális, szerver port> <opcionális, egy kép útvonala> ```<br>
