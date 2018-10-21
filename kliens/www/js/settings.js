// SETTINGS.JS - settings.html-ben használt függvények

window.onload = function() {
    // beállítja az új felhasználónév mezőjének a helyébe a régi felhasználónevet
    var uname = window.localStorage.getItem("UName");
    document.getElementById('unameField').placeholder = uname;
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