/*
*    A probléma az egyNapAnyagai() függvénynél található, ott még részletesebbel leírom, mi a helyzet.
*    Tudom, csomó helyen szükség van egy erős refaktorra, de elsősorban az a célom, hogy működjön.
*/

var got_to_day = false;
var locat = window.location.href;
var AnyagResponse;

window.onload = function() {
    if (/index.html/.test(locat) && got_to_day == false) {
        ezAHetLekerese();
    }
    if (/egy_nap.html/.test(locat) && got_to_day == false) {
        egyNapAnyagai();
    }
}

function removePreviousStatus() {
    try {
    document.getElementById('statusDiv').innerHTML = '';
    } catch(err) {}
}

function success(message) {
    removePreviousStatus();
    var successAlert = document.createElement("DIV");
    successAlert.innerHTML = '<div class="alert alert-sm alert-success">' + message + '</div>';
    document.getElementById('statusDiv').appendChild(successAlert);
}

function info(message) {
    removePreviousStatus();
    var infoAlert = document.createElement("DIV");
    infoAlert.innerHTML = '<div class="alert alert-sm alert-info">' + message + '</div>';
    document.getElementById('statusDiv').appendChild(infoAlert);
}

function error() {
    removePreviousStatus();
    var errAlert = document.createElement("DIV");
    errAlert.innerHTML = '<div class="alert alert-sm alert-danger">Ez a hibaüzi a net hiányáról szól.</div>';
    document.getElementById('statusDiv').appendChild(errAlert);
}

// bejegyzés törlése a kuka gombbal a bejegyzés mellett
function BejegyzTorlese(bejegyzId, bejegyzDiv) {
    $.ajax({
        type: "delete",
        url: getUrl() + "/delete/" + bejegyzId,
        success: function(responseData, textStatus, jqXHR) {
            success('A bejegyzést sikeresen törölted');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });
}

// beállítások menüben történő, id alapú bejegyzéstörlés
function BejegyzTorleseId() {
    $.ajax({
        type: "delete",
        url: getUrl() + "/delete/" + document.getElementById('deleteObj').value,
        success: function(responseData, textStatus, jqXHR) {
            success('A bejegyzést sikeresen törölted');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });
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
    var IPaddress = '46.139.116.9';
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

function ezAHetLekerese() {
    $.ajax({
        type: "get",
        url: getUrl() + '/het/' + getWeek(),
        success: function(responseData, textStatus, jqXHR) {
            responseJSON = JSON.parse(responseData)
            // Összes JSON anyaga
            pufferAnyag = []
            for (i = 0; i < responseJSON.length; i++) {
                pufferAnyag.push(responseJSON[i].anyag);
            }
            //console.log('Összes JSON anyaga: ' + '\n' + pufferAnyag + '\n -----');
            /*document.getElementById("socket").innerHTML += '<h2>' + pufferAnyag + '<h2>';*/

            // Összes JSON napja
            pufferNap = []
            for (i = 0; i < responseJSON.length; i++) {
                pufferNap.push(responseJSON[i].nap);
            }
            napok = pufferNap.unique()
            napok.sort()
            DayDict = {
                0: "Hétfő",
                1: "Kedd",
                2: "Szerda",
                3: "Csütörtök",
                4: "Péntek",
                5: "Szombat",
                6: "Vasárnap"
            }
            var adottNap
            for (i = 0; i < napok.length; i++) {
                adottNap = napok[i];
                document.getElementById('socket').innerHTML += '<button class="btn btn-primary teljesKepernyoBootstrapPrimary" onclick=navigate(' + adottNap + ')>' + DayDict[adottNap] + '</button><br><br>'
            }
            // Ne az összes napot írja ki, hanem mindenből csak egyet (ha van legalább arra a napra bejegyzés)
            //console.log('Összes JSON napja: ' + '\n' + pufferNap.unique() + '\n -----');

            //console.log(JSON.stringify(responseJSON))
        },
        error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });
}

function AnyagLekeres() {
    document.getElementById('socket').innerHTML = '';
    info('Mindegyik hét mutatása');
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

            /*document.getElementById("socket").innerHTML = '<h2>' + responseData + '<h2>';
            //console.log('Első bejegyzés szerkesztője: ' + '\n' + responseJSON[0].uname + '\n -----');*/

            // Összes JSON anyaga
            pufferAnyag = []
            for (i = 0; i < responseJSON.length; i++) {
                pufferAnyag.push(responseJSON[i].anyag);
            }
            //console.log('Összes JSON anyaga: ' + '\n' + pufferAnyag + '\n -----');
            /*document.getElementById("socket").innerHTML += '<h2>' + pufferAnyag + '<h2>';*/

            // Összes JSON napja
            pufferNap = []
            for (i = 0; i < responseJSON.length; i++) {
                pufferNap.push(responseJSON[i].nap);
            }
            napok = pufferNap.unique()
            napok.sort()
            DayDict = {
                0: "Hétfő",
                1: "Kedd",
                2: "Szerda",
                3: "Csütörtök",
                4: "Péntek",
                5: "Szombat",
                6: "Vasárnap"
            }
            var adottNap
            for (i = 0; i < napok.length; i++) {
                adottNap = napok[i];
                document.getElementById('socket').innerHTML += '<button class="btn btn-primary teljesKepernyoBootstrapPrimary" onclick="navigate(' + adottNap + ', true)">' + DayDict[adottNap] + '</button><br><br>'
            }
            // Ne az összes napot írja ki, hanem mindenből csak egyet (ha van legalább arra a napra bejegyzés)
            //console.log('Összes JSON napja: ' + '\n' + pufferNap.unique() + '\n -----');

            //console.log(JSON.stringify(responseJSON))
        },
        error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });
}
var clickedButton;
var url = new URL(window.location.href.replace("index.html", "egy_nap.html")); //URL query param

function navigate(nap, mindegyikHet) {
    //console.log(clickedButton);
    if (mindegyikHet) {
        url.searchParams.append('mindegyikHet', true); //URL query param
    }
    url.searchParams.append('day', nap); //URL query param
    location.href = url; //URL query param
}


function bejegyzesDoboztKreal(divId) {
        document.getElementById("socket").innerHTML += '<div class="well" id="' + divId + '"></div>'
        document.getElementById(divId).innerHTML += '<h2 class="text-muted" style="overflow-wrap: break-word;">' + divId + '</h2>'
}

function bejegyzestKiegeszit(divId, jsonElem) {
        document.getElementById(divId).innerHTML += '<div class="row"><h2 class="col-xs-10" style="overflow-wrap: break-word;">' + jsonElem.anyag + '<span class="badge badge-pill badge-primary">' + jsonElem.uname + '</span></h2><br><button class="btn btn-danger col-xs-2" onclick="BejegyzTorlese(\'' + jsonElem._id.$oid + '\', ' + divId + ')"><span class="glyphicon glyphicon-trash"></span></button></div>'
}


function anyagokLekereseEsMegjelenitese(mindegyikHet) {
    if (mindegyikHet == true) {
        $.ajax({
            type: "get",
            url: getUrl(),
            success: function(responseData, textStatus, jqXHR) {

                // parseoljuk a jsont
                responseJSON = JSON.parse(responseData)

                // itt tárolódnak a megjelenítendő adatok (tantárgyakat a divek id-jének használom)
                anyagTantDict = {tantok:[], anyagok:[], jsonok:[]}
        
                // válogassa ki, melyik bejegyzés szól erre a napra
                for (i=0; i<responseJSON.length; i++) {
                    if (responseJSON[i].nap == clickedButton) {
                        anyagTantDict.tantok.push(responseJSON[i].tant)
                        anyagTantDict.anyagok.push(responseJSON[i].anyag)
                        anyagTantDict.jsonok.push(responseJSON[i])
                    }
                }

                // készítse el a tantárgydobozt a tantárgy címével
                for (i=0; i<anyagTantDict.tantok.unique().length; i++) {
                    bejegyzesDoboztKreal(anyagTantDict.tantok.unique()[i], anyagTantDict.tantok.unique()[i])
                }

                // töltse ki a dobozokat az anyagokkal
                for (i=0; i<anyagTantDict.anyagok.length; i++) {
                    bejegyzestKiegeszit(anyagTantDict.tantok[i], anyagTantDict.jsonok[i])
                }
           },
            error: function(jqXHR, textStatus, errorThrown) {
                error();
            }
        });
    } else {
        $.ajax({
            type: "get",
            url: getUrl() + '/het/' + getWeek(),
            success: function(responseData, textStatus, jqXHR) {

                // parseoljuk a jsont
                responseJSON = JSON.parse(responseData)

                // itt tárolódnak a megjelenítendő adatok (tantárgyakat a divek id-jének használom)
                anyagTantDict = {tantok:[], anyagok:[], jsonok:[]}
        
                // válogassa ki, melyik bejegyzés szól erre a napra
                for (i=0; i<responseJSON.length; i++) {
                    if (responseJSON[i].nap == clickedButton) {
                        anyagTantDict.tantok.push(responseJSON[i].tant)
                        anyagTantDict.anyagok.push(responseJSON[i].anyag)
                        anyagTantDict.jsonok.push(responseJSON[i])
                    }
                }

                // készítse el a tantárgydobozt a tantárgy címével
                for (i=0; i<anyagTantDict.tantok.unique().length; i++) {
                    bejegyzesDoboztKreal(anyagTantDict.tantok.unique()[i], anyagTantDict.tantok.unique()[i])
                }

                // töltse ki a dobozokat az anyagokkal
                for (i=0; i<anyagTantDict.anyagok.length; i++) {
                    bejegyzestKiegeszit(anyagTantDict.tantok[i], anyagTantDict.jsonok[i])
                }
           },
            error: function(jqXHR, textStatus, errorThrown) {
                error();
            }
        });
    }
}

function egyNapAnyagaiMindegyikHet() {
    anyagokLekereseEsMegjelenitese(true);
}

function egyNapAnyagai() {
    var param = new URLSearchParams(window.location.search);
    clickedButton = param.get('day');
    if (param.get('mindegyikHet') == 'true') {
        egyNapAnyagaiMindegyikHet();
    }
    else { // aktuális hét
        anyagokLekereseEsMegjelenitese();
    }
}
