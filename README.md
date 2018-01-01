**Szerver-kliens kapcsolatteszt**<br>
Travis |
[![Build Status](https://travis-ci.org/Sletteon/cm-conntest.svg?branch=master)](https://travis-ci.org/Sletteon/cm-conntest)<br>
Jenkins |
[![Build Status](http://46.139.116.9:9000/buildStatus/icon?job=cm-conntest)](http://46.139.116.9:9000/job/cm-conntest)

*A techtabor/cm-conntest, illetve a sletteon/cm-conntest repository gyakorlatilag ugyanaz, de a travis miatt nem akartam a mentorokat zavarni. Úgy pusholok ide hogy a techtabor repoját cloneolom, rendes commitok mellett nyomok ```git push --mirror https://github.com/sletteon/cm-conntest```-et, és ezután rendes ```git push```t*<br>
*Travis-t használom főleg az automata teszteléshez, de most kísérletezek a Jenkins-el*

**Hasznos linkek**<br>
[PhoneGap dokumentáció](http://docs.phonegap.com/)<br>
[Cordova dokumentáció](https://cordova.apache.org/docs/en/latest/)<br>
[Legstabilabb kliens apk](https://build.phonegap.com/apps/2934479/download/android)<br>
**Függőségek:**<br>
flask, flask_cors, colorama<br>
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
