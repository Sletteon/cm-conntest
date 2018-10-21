// UNAME_CHECK.JS - felhasználónév ellenőrzése, felhasználónév hiányában gyorsan kérünk egyet

window.onload = function() {
    var UName = window.localStorage.getItem("UName");
    // amennyiben nincs felhnév mentve, prompttal kérjen egyet
    if (UName == null) {
        UName = prompt("Add meg a beceneved:");
        window.localStorage.setItem("UName", UName);
        var UName = window.localStorage.getItem("UName");
        success('Új beceneved: ' + UName + '.');
    }

    if (navigator.onLine == false) {
        noInternetMessage();
    }

}