// ha megnyomják ezt a gombot, futtassa le ezt az anonim funkciót
document.getElementById("connButton").onclick = function(){
    // kérje el változókba az IP-t és a portot
    IPaddress = document.getElementById("IP").value;
    Port = document.getElementById("Port").value;
    // rakja össze az IP-t és a portot egy link formájában
    wsURL = "ws://" + IPaddress + ":" + Port + "/";
    // csináljon egy connection objektumot, és nyissa meg az előzőleg összedobott linkkel
    var connection = new WebSocket(wsURL);
    // ha sikeres volt a csatlakozás (beleértve a handshake, amit az http protokoll erőszakol ránk), futtassa le ezt az anonim 
    // funkciót
    connection.onopen = function () { 
        // így alakult a uname változó neve: uname = UserNAME
        // kérje le a létező, vagy nem létező felhnevet
        // (uname itt most a kulcs, ha lekérünk vmi más adatot, 
        // egy általunk kitalált másik kulcsot kell beírni a uname helyett)
        var uname = window.localStorage.getItem("uname");
        // ha van egy uname tárolva, csak küldje el a szervernek azt
        if (uname != null) {
            // FONTOS: a szerver csak egyszerre fogad el adatot, így vesszőkkel kell majd elválasztani a küldendő dolgokat
            // az lenne jó, ha minden küldendő adat után mindig külön kapcsolódik, ugyanis
            // 1. offline elérhetőség 2. máshogy nagyon bonyolult lenne
            connection.send('name: ' + uname);
        } else {
            // amennyiben nincs felhnév mentve, prompttal kérjen egyet
            uname = prompt("Add meg a beceneved:");
            // állítsa be a uname változót a uname kulcshoz
            window.localStorage.setItem("uname", uname);
            // küldje el a szervernek, kik is vagyunk
            connection.send('name: ' + uname);
        }
   };
    // ha vmi hibát kaptunk (még nem fordult elő), írja ki a consoleba
    connection.onerror = function (error) {
       console.log('WebSocket Error ' + error);
    };
    // ha kaptunk vmit a szervertől, írja ki a logba és írja ki a gomb alatt elhelyezett p tagbe
    connection.onmessage = function (e) {
        console.log('Server: ' + e.data);
        document.getElementById("socket").innerHTML = "server: " + e.data;
    };
};
