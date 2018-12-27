// UPLOAD.JS - uplaod.html-ben használt függvények

window.onload = function() {
    offlineAnyagMegjelenites();
    $('#nap li').on('click', function() {
        $('#napButton').prop('innerText', $(this).text().replace(' ', ''));
    });
    $('#tantargy li').on('click', function() {
        $('#tantButton').prop('innerText', $(this).text().replace(' ', ''));
    });
}



// kér egy napot a hétből és ellenőrzi, elmúlt-e már
function isThisDayOfWeekPastToday(dayOfWeek) {
    dayOfWeek = dayOfWeek + 1;
    var d = new Date();
    today = d.getDay();
    if(dayOfWeek<today) {
        return true; // már elmúlt 
    }
    if(dayOfWeek==today) {
        hours = d.getHours()
        if(hours>16) { // délután 4-kor már biztos nem fog senk erre a napra dolgozatot beírni
            return true; // már elmúlt 
        }
    }
    if(dayOfWeek>today) {
        return false; // még nem múlt el
    }
}

// számot csinál a nap szövegéből (0=hétfő, 1=kedd, ... , 5=szombat), hiba esetén 1-t kapunk
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
            return 1;
            break;
    }
}

// ugyan az, mint convertDayTextToNumbers(), csak számokat alakítunk napokká
function convertNumbersToDayText(dayNumber) {
    switch (dayNumber) {
        case 0:
            return 'Hétfő';
            break;
        case 1:
            return 'Kedd';
            break;
        case 2:
            return 'Szerda';
            break;
        case 3:
            return 'Csütörtök';
            break;
        case 4:
            return 'Péntek';
            break;
        case 5:
            return 'Szombat';
            break;
        default:
            return 1;
            break;
    }
}

// lekéri az upload.html elemeiből a szükséges adatot
// és internetelérés állapotától függően küld el, vagy tárol el
function getAllDataAndSubmit() {

    var napText = $('#napButton').text().replace('\n', '');
    var nap = convertDayTextToNumbers(napText);

    if (isThisDayOfWeekPastToday(nap)) {
        var het = getWeek() + 1;
        info('Már elmúlt ez a nap; jövő hétbe írás', true);
    } else {
        var het = getWeek();
    }

    var tantText = $('#tantButton').text().replace('\n', '');
    var sendingJSON = {
        "uname": window.localStorage.getItem("UName"),
        "het": het,
        "nap": nap,
        "tant": tantText,
        "anyag": document.getElementById("anyag").value,
        "pic": ""
    };


    if (navigator.onLine == true) {
        submitMaterial(getUrl(), JSON.stringify(sendingJSON), function() {
            success('Bejegyzés elküldve', true);
        });
    } else {
        noInternetMessage();
        if (window.localStorage.getItem('storedJSONs') == null) {
            var tempJSON = [];
            window.localStorage.setItem('storedJSONs', JSON.stringify(tempJSON));
        }
        var storedJSONs = [];
        storedJSONs = JSON.parse(window.localStorage.getItem('storedJSONs'));
        storedJSONs.push(sendingJSON);
        console.log(JSON.stringify(storedJSONs));
        window.localStorage.setItem('storedJSONs', JSON.stringify(storedJSONs));
        offlineAnyagMegjelenites();
    }
}

// elküldi a mentett bejegyzéseket
function submitSavedMaterial() {
    var sendingJSON = JSON.stringify(window.localStorage.getItem('storedJSONs'));
    submitMaterial(sendingJSON);
    if (navigator.onLine == true) {
        offlineAnyagTorles();
    }
}

// eldobja a mentett bejegyzéseket
function offlineAnyagTorles() {
    window.localStorage.removeItem('storedJSONs')
}

// egy mentett bejegyzést töröl
function egyOfflineAnyagTorles(tant, anyag) {
    storedJSONs = JSON.parse(window.localStorage.getItem('storedJSONs'));

    storedJSONs.forEach( function(element, index){
        if (element['tant'] == tant && element['anyag'] == anyag) {
            storedJSONs.splice(index, 1);
        }
    });

    window.localStorage.setItem('storedJSONs', JSON.stringify(storedJSONs));
    offlineAnyagMegjelenites();
}

// megjeleníti a mentett adatokat a savedDataDiv-be
function offlineAnyagMegjelenites() {
    storedJSONs = JSON.parse(window.localStorage.getItem('storedJSONs'));
    if (storedJSONs=="" || storedJSONs==null) {
        return;
    } else {
        document.getElementById('savedDataDiv').innerHTML="";
    }
    storedJSONs.forEach(element => {
        console.log(element)
        appendElem = document.createElement('DIV');
        appendElem.classList.add('row')
        appendElem.innerHTML = '<h4 class="col-xs-8"> (' + convertNumbersToDayText(element['nap']) + ') ' + element['tant'] + ": " + element['anyag'] + "</h4>";
        appendElem.innerHTML += '<button class="btn btn-danger col-xs-3" onclick="egyOfflineAnyagTorles(\'' + element['tant'] + '\',\'' + element['anyag'] + '\')"><span class="glyphicon glyphicon-trash"></span></button></div>'
        document.getElementById('savedDataDiv').appendChild(appendElem);
    });

}