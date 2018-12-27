// SETTINGS.JS - settings.html-ben használt függvények

window.onload = function() {
    // beállítja az új felhasználónév mezőjének a helyébe a régi felhasználónevet
    var uname = window.localStorage.getItem("UName");
    document.getElementById('unameField').placeholder = uname;

    var IP = window.localStorage.getItem("serverIp");
    var port = window.localStorage.getItem("serverPort");

    if (IP == undefined) {
        IP = "46.139.116.9";
    }

    if (port == undefined) {
        port = 8000;
    }

    document.getElementById("serverIpField").value = IP;
    document.getElementById("serverPortField").value = port;
}

// a régi felhasználónév helyébe menti az új felhasználónév mezőjének szövegét
function updateUsername() {
    window.localStorage.removeItem("UName");
    window.localStorage.setItem("UName", document.getElementById("unameField").value);
    success('Új beceneved: ' + window.localStorage.getItem("UName"));
}

// beállítások menüben történő, id alapú bejegyzéstörlés
function getIdAndDeleteMaterial() {
    var idToDelete = document.getElementById('deleteObj').value;
    deleteMaterial(getUrl(), idToDelete);
}

function updateIP() {
    window.localStorage.removeItem("serverIp");
    window.localStorage.removeItem("serverPort");
    window.localStorage.setItem("serverIp", document.getElementById("serverIpField").value);
    window.localStorage.setItem("serverPort", document.getElementById("serverPortField").value);
    success('Új szerver url: ' + window.localStorage.getItem("serverIp") + ":" + window.localStorage.getItem("serverPort"));
}