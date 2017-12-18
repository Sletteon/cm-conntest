**Szerver-kliens kapcsolatteszt**<br><br>
**Hasznos linkek**<br>
[PhoneGap dokumentáció](http://docs.phonegap.com/)<br>
[Cordova dokumentáció](https://cordova.apache.org/docs/en/latest/)<br>
<!-- [Legstabilabb kliens apk](https://build.phonegap.com/apps/2893794/download/android/?qr_key=a5nry2YDex911S8dvqJu)<br> -->
**Függőségek:**<br>
flask, flask_cors<br>v
**Szerver:**<br>
Amikor a szerverre csatlakozik valaki, megnézi, amennyiben GET eljárást használ a kliens, valószínűleg le szeretné kérni az elmentett adatokat,
így azokat JSON formátumban elküldi a szerver.
Ha viszont a kliens küldi el az adatokat, azt a szervernek POST metódusával teszi, szintén JSON-ban.

Példa az anyagbeállításra:<br>

```
{
	"uname":"misi",
	"het":"E",
	"nap":"K",
	"tant":"töri",
	"anyag":"frank birodalom"
}
```
<br>
Ahol misi a felhasználónév, amit első indításnál elkér a weboldal, [E]z a hét [K]edden töriből a frank birodalom lesz a tananyag.<br>

Napok: [H]étfő | [K]edd | [S]zerda | [C]sütörtök | [P]éntek<br>
Hetek: [E]z a hét [J]övő hét<br>

**Kliens:**<br>
A klienst a PhoneGap programmal, HTML, JS illetve CSS nyelveken írjuk.<br>
A program ezt a weboldalt (index.html) mobil alkalmazásra fogja fordítani [ezen](https://build.phonegap.com) az oldalon.<br>
Debuggolás folyamata a böngészőben történik a fejlesztői eszközök miatt.<br>
index.html helye: /kliens/www/index.html<br>
A felhasználó be tud adni adatot, le tud kérni adatot, mindezeket külön gombokkal.<br>
Valamint a gombok alatt, egy link, megnyomása a felhasználónév törlésével, illetve a weboldal újratöltésével jár.<br>
