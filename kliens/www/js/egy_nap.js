window.onload = function() {
    // nézzük meg, melyik napot kell lekérnünk ill. melyik (egy megadott/az összes) hét napját kérjük le
    var param = new URLSearchParams(window.location.search);
    clickedButton = param.get('day');
    if (param.get('allWeek') == 'true') {
        getMaterialDependingOnWeek(true);
    }
    else { // aktuális hét
        getMaterialDependingOnWeek(false);
    }
}

// létrehozza az anyagot tároló dobozt
function createMaterialWell(divId) {
    document.getElementById("socket").innerHTML += '<div class="well" id="' + divId + '"></div>';
    document.getElementById(divId).innerHTML += '<h2 class="text-muted" style="overflow-wrap: break-word;">' + divId + '</h2>';
}

// kitölti a megadott id-jű dobozt a megadott bejegyzés jsonjával
function fillMaterialWell(divId, jsonElem) {
    document.getElementById(divId).innerHTML += '<div class="row"><h3 class="col-xs-10" style="overflow-wrap: break-word;"><span class="badge badge-pill badge-primary">' + jsonElem.uname + '</span>' + jsonElem.anyag + '</h3><br><button class="btn btn-danger col-xs-2" onclick="deleteMaterial(\'' + getUrl() + '\', \'' + jsonElem._id.$oid + '\')"><span class="glyphicon glyphicon-trash"></span></button></div>';
}

// egyesével hozza létre, majd töltse ki a bejegyzések dobozát
function showMaterials(responseJSON) {
    // itt tárolódnak a megjelenítendő adatok (tantárgyakat a divek id-jének használom)
    anyagTantDict = {tantok:[], anyagok:[], jsonok:[]};
    
    // válogassa ki, melyik bejegyzés szól erre a napra
    for (i=0; i<responseJSON.length; i++) {
        if (responseJSON[i].nap == clickedButton) {
            anyagTantDict.tantok.push(responseJSON[i].tant);
            anyagTantDict.anyagok.push(responseJSON[i].anyag);
            anyagTantDict.jsonok.push(responseJSON[i]);
        }
    }
    
    // készítse el a tantárgydobozt a tantárgy címével
    for (i=0; i<anyagTantDict.tantok.unique().length; i++) {
        createMaterialWell(anyagTantDict.tantok.unique()[i], anyagTantDict.tantok.unique()[i]);
    }
    
    // töltse ki a dobozokat az anyagokkal
    for (i=0; i<anyagTantDict.anyagok.length; i++) {
        fillMaterialWell(anyagTantDict.tantok[i], anyagTantDict.jsonok[i]);
    }

}

// jelenítse meg az anyagokat a HTML-ben
function getMaterialDependingOnWeek_successFunction(responseData) {
    responseJSON = JSON.parse(responseData);
    showMaterials(responseJSON);
}

// ha csak az e heti anyagokat kértük le, írjuk be a localStorage-be
// mindenesetben hívjuk meg a getMaterialDependingOnWeek_successFunction() függvényt
function getMaterialDependingOnWeek(allWeek) {
    if (allWeek == true) {
        getMaterial(getUrl(), false, function(responseData, textStatus, jqXHR){
            getMaterialDependingOnWeek_successFunction(responseData);
        });
    } else {
        getMaterialCustomError(getUrl(), getWeek(), function(responseData, textStatus, jqXHR) {
            getMaterialDependingOnWeek_successFunction(responseData);
        }, function(jqXHR, textStatus, errorThrown) {
            noInternetMessage();
            var thisWeekData = window.localStorage.getItem('thisWeekData')
            if(thisWeekData != null){
                showMaterials(JSON.parse(thisWeekData));
            } else{
                error();
            }
        });
    }
}