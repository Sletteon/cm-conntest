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
    document.getElementById(bejegyzDiv).remove()
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

function egyNapAnyagaiMindegyikHet() {
    $.ajax({
        type: "get",
        url: getUrl(),
        success: function(responseData, textStatus, jqXHR) {
            responseJSON = JSON.parse(responseData)

            for (i = 0; i < responseJSON.length; i++) {
                if (responseJSON[i].nap == clickedButton) {
                    /*console.log(clickedButton);*/
                    //console.log(responseJSON[i].nap);
                    document.getElementById("socket").innerHTML += '<div class="well" id="' + i + '"></div>'
                    document.getElementById(i).innerHTML += '<div class="pull-right"><button class="btn btn-danger" onclick="BejegyzTorlese(\'responseJSON[i]._id.$oid, ' + i + ')"><span class="glyphicon glyphicon-trash"></span></button></div>'
                    document.getElementById(i).innerHTML += '<h2 style="overflow-wrap: break-word;">' + responseJSON[i].het + '. hét</h2>'
                    document.getElementById(i).innerHTML += '<h2 style="overflow-wrap: break-word;">Tantárgy: ' + responseJSON[i].tant + '</h2>'
                    document.getElementById(i).innerHTML += '<h2 style="overflow-wrap: break-word;">Anyag: ' + responseJSON[i].anyag + '</h2>'
                }
            }
            //console.log(JSON.stringify(responseJSON))
        },
        error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });
}

// leelenőrzi, hogy egy objektum megtalálható-e egy tömbben
// nekem egy dict listájában kell utánanéznem, nem szimpla listában, így nem vagyok biztos, hogy megfelel-e erre a feladatra
function containsObject(obj, list) {
    var x;
    for (x in list) {
        if (list.hasOwnProperty(x) && list[x] === obj) {
            return true;
        }
    }

    return false;
}

function bejegyzesDoboztKreal(divId) {
    document.getElementById("socket").innerHTML += '<div class="well" id="' + divId + '"></div>'
}

// kiírja a bejegyzésdoboz tantárgyát (címét), valamint az első napot, ami ehhez a tantárgyhoz van rendelve
function bejegyzestMegjelenit(divId, jsonElem, anyag) {
    if (jsonElem.nap == clickedButton) {
        document.getElementById(divId).innerHTML += '<div class="pull-right"><button class="btn btn-danger" onclick="BejegyzTorlese(\'' + jsonElem._id.$oid + '\', ' + i + ')"><span class="glyphicon glyphicon-trash"></span></button></div>'
        document.getElementById(divId).innerHTML += '<h2 style="overflow-wrap: break-word;">Tanárgy: ' + jsonElem.tant + '</h2>'
        document.getElementById(divId).innerHTML += '<h2 style="overflow-wrap: break-word;">Anyag: ' + jsonElem.anyag + '</h2>'
    }
}

// ha esetleg több nap jár 1 tantárgyhoz, írja a dobozának végébe, természetesen a törlés gombbal
function bejegyzestKiegeszit(divId, jsonElem) {
    if (jsonElem.nap == clickedButton) {
        document.getElementById(divId).innerHTML += '<div class="pull-right"><button class="btn btn-danger" onclick="BejegyzTorlese(\'' + jsonElem._id.$oid + '\', ' + i + ')"><span class="glyphicon glyphicon-trash"></span></button></div>'
        document.getElementById(divId).innerHTML += '<h2 style="overflow-wrap: break-word;">' + jsonElem.anyag + '</h2>'
    }
}

/*
*   Az a célom, tantárgyak szerint rendszerezve legyenek a bejegyzések kiírva.
*   Ha pl. hétfőre van 2 bejegyzésünk ami torire vonatkozik, akkor 1 div legyen, ahol fel vannak sorolva az anyagok.
*/
function egyNapAnyagai() {
    var param = new URLSearchParams(window.location.search);
    clickedButton = param.get('day');
    if (param.get('mindegyikHet') == 'true') {
        egyNapAnyagaiMindegyikHet();
    }
    else { // aktuális hét
        $.ajax({
            type: "get",
            url: getUrl() + '/het/' + getWeek(),
            success: function(responseData, textStatus, jqXHR) {

                // parseoljuk a jsont
                responseJSON = JSON.parse(responseData)

                // egy lista, ami dictionary-kat fog tartani, így összekötünk 1 tantárgyat 1 divvel
                tantDivDict = [];

                // végigmegyünk a kapott json-on, hogy ellenőrizzük, be van-e már írva ez a tantárgy
                for (i = 0; i < responseJSON.length; i++) {
                    console.log(i)

                    // ha nincs még beírva, csinálja meg ezt a divet és írja be a bejegyzést
                    // PROBLÉMA 1: hogyan lehet ellenőrizni, hogy egy string benne van-e egy listának elemének elemében
                    // (szerepel-e az éppen ellenőrizendő tantárgy a tantDivDict bármelyik dictjében)
                    if (!responseJSON[i].tant in tantDivDict) {
                           tantDivDict.push({tant:responseJSON[i].tant, div:i})
                           bejegyzesDoboztKreal(i)
                           bejegyzestMegjelenit(i, responseJSON[i], responseJSON[i].anyag)
                    } else {

                        // ha már be van írva a listánkba ez a tantárgy, nézzük meg, milyen ID-vel rendelkezik a tantárgy és írjuk be
                        console.log('tantárgy nincs a tantDivDictben')
                        // PROBLÉMA 2: hogyan tudom megnézni egy bizonyos tantárgyhoz rendelt div id-jét
                        //bejegyzestKiegeszit(tantDivDict, responseJSON[i]);
                    }
                }

            },
            error: function(jqXHR, textStatus, errorThrown) {
                error();
            }
        });
    }
}
