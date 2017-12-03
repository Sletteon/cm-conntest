window.onload = function() {
    var uName = window.localStorage.getItem("uName");
	// amennyiben nincs felhnév mentve, prompttal kérjen egyet
    if (uName == null) {
        uName = prompt("Add meg a beceneved:");
        window.localStorage.setItem("uName", uName);
    }
    // mikor betöltődik az oldal, állítsa be a mutató kurzort a
    // felhnév törléshez, és fehéret a kapcsolódás állapot szövegéhez
    document.getElementById("unameDel").style.cursor = "pointer";
    document.getElementById("connState").style.color = "white";

	// kérje le a napot, és állítsa be a nap ID-jű selectet
    var d = new Date();
    var n = d.getDay();

    switch (n) {
        case 0:
            document.getElementById("nap").value = "K";
            break;
        case 1:
            document.getElementById("nap").value = "H";
            break;
        case 2:
            document.getElementById("nap").value = "K";
            break;
        case 3:
            document.getElementById("nap").value = "S";
            break;
        case 4:
            document.getElementById("nap").value = "C";
            break;
        case 5:
            document.getElementById("nap").value = "P";
            break;
        case 6:
            document.getElementById("nap").value = "K";
            break;
    }
}
// ha az online paraméter igaz, legyen zöld a connState,
// de ha hamis, legyen piros
// ja, meg írja ki a kapcsolódási állapotot
function networkStatus(online) {
    if (online) {
        document.getElementById("connState").style.backgroundColor = "LimeGreen";
        document.getElementById("connState").innerHTML = "Online";
    }
    if (online === false) {
        document.getElementById("connState").style.backgroundColor = "red";
        document.getElementById("connState").innerHTML = "Offline";
    }
}

function conn(message, set) {
    // kérje el változókba az IP-t és a portot
    var IPaddress = document.getElementById("IP").value;
    var Port = document.getElementById("Port").value;
    // kérje le a felhnevet
    var uName = window.localStorage.getItem("uName");
    // ez a hét, vagy a jövő hét
    var h = document.getElementById("het");
    var het = h.options[h.selectedIndex].value;
    try {
        // rakja össze az IP-t és a portot egy link formájában
        var wsURL = "ws://" + IPaddress + ":" + Port + "/";
        // csináljon egy connection objektumot, és nyissa meg az előzőleg összedobott linkkel
        var connection = new WebSocket(wsURL);
    } catch (err) {
        alert('Hiba:' + err)
    }
    // ha kapcsolat létesült
    connection.onopen = function() {
        // ha a set boolean igaz, küldje el a message paramétert set-tel
        // ellenben, ha hamis, gettel küldje el
        if (set) {
            connection.send(uName + ';set;' + het + ';' + message);
            networkStatus(true);
            connection.close();
            networkStatus(false);
        } else {
            connection.send(uName + ';get;' + het + ';');
            networkStatus(true)
            // ha bezárjuk a kapcsolatot, csak 1 parancsot kapunk vissza
            // connection.close();
        }
    };
    // ha vmi hibát kaptunk, írja ki a consoleba
    // nem valami hasznos, mert csak  ezt írja ki: [Socket object]
    connection.onerror = function(error) {
        console.log('WebSocket hiba ' + error);
    };
    // ha kaptunk vmit a szervertől, írja ki a logba és írja ki a gombok alatti p tagbe
    connection.onmessage = function(e) {
        networkStatus(true);
        var gotList = [];
        console.log(e.data);
        gotList.push(e.data);
        document.getElementById("socket").innerHTML = gotList;
    };
    return uName + ';set;' + het + ';' + message;
}
// ha le akarjuk kérni, mi történt ezen a héten, hívja meg a conn funkciót
// üres message-vel, illetve mi nem szeretnénk vmit beállítani, csak lekérdezni
document.getElementById("getButton").onclick = function() {
    conn("", false);
}
// ha megnyomják ezt a gombot, futtassa le ezt az anonim funkciót
document.getElementById("connButton").onclick = function() {
    // nap illetve a hét lekérése
    var n = document.getElementById("nap");
    var nap = n.options[n.selectedIndex].value;
    // tantárgy, anyag
    var tant = document.getElementById("tantargy").value;
    var anyag = document.getElementById("anyag").value;
    // minden megadott adat egyesítése, illetve ezek elválasztása pontosvesszővel
    var mess = nap + ';' + tant + ';' + anyag + ';'
    // végül hívja meg a conn funkciót az előbb összeállított stringgel,
    // és most be szeretnénk írni vmi a szerverre

    document.getElementById("socket").innerHTML = conn(mess, true);

};
// ha a gombok alatti szövegre kattintanak, törölje a felhasználónevet,
// és frissítse az oldalt
document.getElementById("unameDel").onclick = function() {
    window.localStorage.removeItem("uname");
    location.reload(false);
};
