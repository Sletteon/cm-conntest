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

function removePreviousStatus() {
    try {
    document.getElementById('statusDiv').innerHTML = ''; 
    } catch(err) {}
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

function getUrl() {
    var IPaddress = "46.139.116.9";
    var Port = 5000;

    return "http://" + IPaddress + ":" + Port;
}

// https://coderwall.com/p/nilaba/simple-pure-javascript-array-unique-method-with-5-lines-of-code
// Ha egy listában több ugyanolyan elem is megtalálható, csak egy ilyen elemet adjon vissza

// napok lekérésénél lehet hasznos
Array.prototype.unique = function() {
    return this.filter(function(value, index, self) {
        return self.indexOf(value) === index;
    });
}


function AnyagLekeres() {
    $.ajax({
        type: "get",
        url: getUrl(),
        success: function(responseData, textStatus, jqXHR) {
            responseJSON = JSON.parse(responseData)

            // JSON KIBONTÁS

            // uname: felhasználónév (string)
            // het: hét (integer)
            // nap: nap (char) (JS szerint a char is string)
            // tant: tantárgy (string)
            // anyag: anyag (string)

            // JSON-lista első JSON-jának elérése: responseJSON[0]
            // JSON-ban a tantárgy elérése: responseJSON.tant

            document.getElementById("socket").innerHTML = '<h2>' + responseData + '<h2>';
            //console.log('Első bejegyzés szerkesztője: ' + '\n' + responseJSON[0].uname + '\n -----');

            // Összes JSON anyaga
            pufferAnyag = []
            for (i = 0; i < responseJSON.length; i++) {
                pufferAnyag.push(responseJSON[i].anyag);
            }
            //console.log('Összes JSON anyaga: ' + '\n' + pufferAnyag + '\n -----');

            // Összes JSON napja
            pufferNap = []
            for (i = 0; i < responseJSON.length; i++) {
                pufferNap.push(responseJSON[i].nap);
            }
            // Ne az összes napot írja ki, hanem mindenből csak egyet (ha van legalább arra a napra bejegyzés)
            //console.log('Összes JSON napja: ' + '\n' + pufferNap.unique() + '\n -----');
            document.getElementById('socket').innerHTML = '<h2>Napok: </h2>' + pufferNap.unique()

            //console.log(JSON.stringify(responseJSON))
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Hiba a kapcsolat létesítésekor. (lásd konzol)");
        }
    });
}

function convertDayTextToNumbers(text) {
    textStripped = text.replace(' ', '');
    switch (textStripped) {
        case 'Hétfő':
            return 0;
            break;
        case 'Kedd':
            return 1;
            break;
        case 'Szerda':
            return 2;
            break;
        case 'Csütörtök':
            return 3;
            break;
        case 'Péntek':
            return 4;
            break;
        case 'Szombat':
            return 5;
            break;

        default:
            //console.log(text);
            return 1;
            break;
    }

}

function AnyagKuldes(sendingJSON) {
    $.ajax({
        type: "post",
        url: getUrl(),
        data: sendingJSON,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(responseData, textStatus, jqXHR) {
            success('A bejegyzést sikeresen elküldted');
        },
            error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });

}
function offlineAnyagBeallitas() {
    var sendingJSON = JSON.stringify(window.localStorage.getItem('storedJSONs'))
    console.log(JSON.stringify(sendingJSON))
    AnyagKuldes(sendingJSON)
    offlineAnyagTorles()
}

function offlineAnyagTorles() {
    window.localStorage.removeItem('storedJSONs')
}

function offlineAnyagMegjelenites() {
    storedJSONs = JSON.parse(window.localStorage.getItem('storedJSONs'));
    if (storedJSONs==null) {
        return;
    } else {
        document.getElementById('savedDataDiv').innerHTML="";
    }
    storedJSONs.forEach(element => {

        appendElem = document.createElement('H4');
        appendElem.innerHTML = element['tant'] + ": " + element['anyag'];
        document.getElementById('savedDataDiv').appendChild(appendElem);
    });

}

// kér egy napot a hétből és ellenőrzi, elmúlt-e már
function isThisDayOfWeekPastToday(dayOfWeek) {
    var d = new Date();
    today = d.getDay()

    if(dayOfWeek<today) {
        return true; // már elmúlt 
    } else if(dayOfWeek==today) {
        hours = d.getHours()
        if(hours>16) { // délután 4-kor már biztos nem fog senk erre a napra dolgozatot beírni
            return true; // már elmúlt 
        }
    } else {
        return false; // még nem múlt el
    }
}

function AnyagBeallitas() {

    var napSelect = document.getElementById("nap");
    //var nap = napSelect.options[napSelect.selectedIndex].value;

    var napText = $('#napButton').text().replace('\n', '');
    var nap = convertDayTextToNumbers(napText);

    // var hetSelect = document.getElementById("het");
    // var het = hetSelect.options[hetSelect.selectedIndex].value;

    if (isThisDayOfWeekPastToday(nap)) {
        var het = getWeek() + 1;
        info('Már elmúlt ez a nap; jövő hétbe írás')
    } else {
        var het = getWeek();
    }

    var tantText = $('#tantButton').text().replace('\n', '');
    console.log(tantText)

    var sendingJSON = {
        "uname": window.localStorage.getItem("UName"),
        "het": het,
        "nap": nap,
        "tant": tantText,
        "anyag": document.getElementById("anyag").value,
        "pic": getImage()
    };


    if (navigator.onLine == true) {
        AnyagKuldes(JSON.stringify(sendingJSON));
    } else {
        noInternetMessage();
        if (window.localStorage.getItem('storedJSONs') == null) {
            var tempJSON = [];
            window.localStorage.setItem('storedJSONs', JSON.stringify(tempJSON))
        }
        var storedJSONs = [] 
        storedJSONs = JSON.parse(window.localStorage.getItem('storedJSONs'))
        storedJSONs.push(sendingJSON)
        console.log(JSON.stringify(storedJSONs))
        window.localStorage.setItem('storedJSONs', JSON.stringify(storedJSONs))
    }
}


// kiralzolja a picSelectben kiválasztott képet
function draw() {
    canvas = document.getElementById('picCanvas')
    select = document.getElementById('picSelect')

    var ctx = canvas.getContext('2d'),
        img = new Image(),
        f = select.files[0],
        url = window.URL || window.webkitURL,
        src = url.createObjectURL(f);
    img.src = src;
    canvas.width = f.width;
    canvas.height = f.height;
    img.onload = function() {
        //alert(img.width + " " + img.height)
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvas.width, canvas.height);
        url.revokeObjectURL(src);
    }
}

// A canvasra kirajzolt képet adja vissza base64 kódolásban, tejles minőségben
function getImage() {
    try {
        var pictureMIMEtype = document.getElementById("picSelect").files[0].type;
    } catch (TypeError) {
        return '';
    }
    //alert(pictureMIMEtype);
    return pic = document.getElementById("picCanvas").toDataURL(pictureMIMEtype, 1.0);
}

// ha kiválasztottak egy kép-fájlt
/*document.getElementById("picSelect").addEventListener("change", draw, false);

  document.getElementById("getButton").onclick = function() {
  AnyagLekeres();
  };*/

try{
    document.getElementById("objDelButton").onclick = function() {
        BejegyzTorlese();
    };
} catch(e){}

try{
    document.getElementById("connButton").onclick = function() {
        AnyagBeallitas();
    };
} catch(e){}


