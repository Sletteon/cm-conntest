window.onload = function(){
	// így alakult a uname változó neve: uname = UserNAME
        // kérje le a létező, vagy nem létező felhnevet
        // (uname itt most a kulcs, ha lekérünk vmi más adatot, 
        // egy általunk kitalált másik kulcsot kell beírni a uname helyett)
        var uname = window.localStorage.getItem("uname");
        if (uname == null) {
            // amennyiben nincs felhnév mentve, prompttal kérjen egyet
            uname = prompt("Add meg a beceneved:");
            // állítsa be a uname változót a uname kulcshoz
            window.localStorage.setItem("uname", uname);
        }
}

function conn(message, set) {
    // kérje el változókba az IP-t és a portot
    var IPaddress = document.getElementById("IP").value;
    var Port = document.getElementById("Port").value;
    // kérje le a felhnevet
    var uname = window.localStorage.getItem("uname"); 
    // ez a hét, vagy a jövő hét
    var h = document.getElementById("het");
    var het = h.options[h.selectedIndex].value;

    try {
        // rakja össze az IP-t és a portot egy link formájában
        var wsURL = "ws://" + IPaddress + ":" + Port + "/";
        // csináljon egy connection objektumot, és nyissa meg az előzőleg összedobott linkkel
        var connection = new WebSocket(wsURL);}
        catch (err){
       alert('Hiba:' + err)
    } 
        // ha kapcsolat létesült
        connection.onopen = function () { 
        // ha a set boolean igaz, küldje el a message paramétert set-tel
        // ellenben, ha hamis, gettel küldje el
	   if (set){
	    connection.send(uname + ';set;' + het + ';' + message);
            connection.close()
	   }else{
                connection.send(uname + ';get;' + het + ';');
	   }
       };
        // ha vmi hibát kaptunk, írja ki a consoleba
        // nem valami hasznos, mert csak  ezt írja ki: [Socket object]
        connection.onerror = function (error) {
           console.log('WebSocket hiba ' + error);
        };
        // ha kaptunk vmit a szervertől, írja ki a logba és írja ki a gombok alatti p tagbe
        connection.onmessage = function (e) {
            console.log('Szerver: ' + e.data);
    	    document.getElementById("socket").innerHTML = e.data;
            connection.close()
        };
    return uname + ';set;' + het + ';' + message;
}
// ha le akarjuk kérni, mi történt ezen a héten, hívja meg a conn funkciót
// üres message-vel, illetve mi nem szeretnénk vmit beállítani, csak lekérdezni
document.getElementById("getButton").onclick = function(){
	conn("",false);
}
// ha megnyomják ezt a gombot, futtassa le ezt az anonim funkciót
document.getElementById("connButton").onclick = function(){
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
    // conn(mess,true);

    document.getElementById("socket").innerHTML = conn(mess,true);
    
};
