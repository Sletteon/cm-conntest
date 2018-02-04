window.onload = function() {
    var UName = window.localStorage.getItem("UName");
    // amennyiben nincs felhnév mentve, prompttal kérjen egyet
    if (UName == null) {
        UName = prompt("Add meg a beceneved:");
        window.localStorage.setItem("UName", UName);
    }


}

// visszaadja a mai napnak a berűkódját
function getDay() {

    var dateObj = new Date();
    var nap = dateObj.getDay();

    switch (nap) {
        case 0:
            return "K";
            break;
        case 1:
            return "H";
            break;
        case 2:
            return "K";
            break;
        case 3:
            return "S";
            break;
        case 4:
            return "C";
            break;
        case 5:
            return "P";
            break;
        case 6:
            return "K";
            break;
    }
}

function getWeek() {
    // Hét száma az évben
    Date.prototype.getWeekNumber = function() {
        var d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()))
        var dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
    };
	return new Date().getWeekNumber();
}

function getUrl/*HardCoded*/() {
    var IPaddress = 'localhost'; /*document.getElementById("IP").value;*/
    var Port = 5000; /*document.getElementById("Port").value;*/

    return "http://" + IPaddress + ":" + Port;
}

function getUrlS/*oftCoded*/() {
	var IPaddress = document.getElementById("IP").value;
    var Port = document.getElementById("Port").value;

    return "http://" + IPaddress + ":" + Port;
}

function AnyagLekeres() {
    $.ajax({
        type: "get",
        url: getUrl(),
        success: function(responseData, textStatus, jqXHR) {
            document.getElementById("socket").innerHTML = '<h2>' + responseData + '<h2>';
            console.log('Szerver: ' + '\n' + responseData + '\n -----');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Hiba a kapcsolat létesítésekor. (lásd konzol)");
        }
    });
}

function AnyagBeallitas() {

    var napSelect = document.getElementById("nap");
    var nap = napSelect.options[napSelect.selectedIndex].value;

    var hetSelect = document.getElementById("het");
    var het = hetSelect.options[hetSelect.selectedIndex].value;

    var sendingJSON = {
        "uname": window.localStorage.getItem("UName"),
        "het": getWeek(),
        "nap": getDay(),
        "tant": document.getElementById("tantargy").value,
        "anyag": document.getElementById("anyag").value
    };
    console.log('Küldendő: ' + '\n' + JSON.stringify(sendingJSON) + '\n -----');

    $.ajax({
        type: "post",
        url: getUrl(),
        data: JSON.stringify(sendingJSON),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(responseData, textStatus, jqXHR) {},
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Hiba a kapcsolat létesítésekor. (lásd konzol)");
        }
    });
}

document.getElementById("getButton").onclick = function() {
    AnyagLekeres();
};

document.getElementById("connButton").onclick = function() {
    AnyagBeallitas();
};
// ha a gombok alatti szövegre kattintanak, törölje a felhasználónevet,
// és frissítse az oldalt
document.getElementById("unameDel").onclick = function() {
    window.localStorage.removeItem("UName");
    location.reload(false);
};
