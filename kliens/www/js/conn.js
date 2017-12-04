window.onload = function() {
    var UName = window.localStorage.getItem("UName");
	// amennyiben nincs felhnév mentve, prompttal kérjen egyet
    if (UName == null) {
        UName = prompt("Add meg a beceneved:");
        window.localStorage.setItem("UName", UName);
    }
    // mikor betöltődik az oldal, állítsa be a mutató kurzort a
    // felhnév törléshez, és fehéret a kapcsolódás állapot szövegéhez
    document.getElementById("unameDel").style.cursor = "pointer";
    document.getElementById("connState").style.color = "white";

	// kérje le a napot, és állítsa be a nap ID-jű selectet
    var dateObj = new Date();
    var nap = dateObj.getDay();

    switch (nap) {
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

function connect(message, set) {

    var IPaddress = document.getElementById("IP").value;
    var Port = document.getElementById("Port").value;

    var UName = window.localStorage.getItem("UName");

    var hetSelect = document.getElementById("het");
    var het = hetSelect.options[hetSelect.selectedIndex].value;

    try {
        var wsURL = "ws://" + IPaddress + ":" + Port + "/";
        // csináljon egy connection objektumot, és nyissa meg az előzőleg összedobott linkkel
        var connection = new WebSocket(wsURL);

    } catch (err) {
        alert('Hiba:' + err)
    }

    connection.onopen = function() {
        if (set) {
            connection.send(UName + ';set;' + het + ';' + message);
            networkStatus(true);

            connection.close();
            networkStatus(false);

        } else {
            connection.send(UName + ';get;' + het + ';');
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
    connection.onmessage = function(gotMessage) {
        networkStatus(true);

        var gotList = [];
        console.log(gotMessage.data);
        gotList.push(gotMessage.data);

        document.getElementById("socket").innerHTML = gotList;
    };
    return UName + ';set;' + het + ';' + message;
}
// ha le akarjuk kérni, mi történt ezen a héten, hívja meg a connect funkciót
// üres message-vel, illetve mi nem szeretnénk vmit beállítani, csak lekérdezni
document.getElementById("getButton").onclick = function() {
    connect("", false);
}
// ha megnyomják ezt a gombot, futtassa le ezt az anonim funkciót
document.getElementById("connButton").onclick = function() {
    // nap illetve a hét lekérése
    var napSelect = document.getElementById("nap");
    var nap = napSelect.options[napSelect.selectedIndex].value;
    // tantárgy, anyag
    var tant = document.getElementById("tantargy").value;
    var anyag = document.getElementById("anyag").value;
    // minden megadott adat egyesítése, illetve ezek elválasztása pontosvesszővel
    var mess = nap + ';' + tant + ';' + anyag + ';'
    // végül hívja meg a connect funkciót az előbb összeállított stringgel,
    // és most be szeretnénk írni vmi a szerverre

    document.getElementById("socket").innerHTML = connect(mess, true);

};
// ha a gombok alatti szövegre kattintanak, törölje a felhasználónevet,
// és frissítse az oldalt
document.getElementById("unameDel").onclick = function() {
    window.localStorage.removeItem("UName");
    location.reload(false);
};
