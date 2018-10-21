var got_to_day = false;
var locat = window.location.href;
var AnyagResponse;



// bejegyzés törlése a kuka gombbal a bejegyzés mellett
function egy_nap_deleteMaterial(bejegyzId, bejegyzDiv) {
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


// index.html-ben a napok gombjainak megjelenítése
function ezAHetLekerese() {
    $.ajax({
        type: "get",
        url: getUrl() + '/het/' + getWeek(),
        success: function(responseData, textStatus, jqXHR) {
            responseJSON = JSON.parse(responseData)
            window.localStorage.setItem('thisWeekData', responseData)
            indexNapiGombokMegjelenitese(responseJSON, false);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            noInternetMessage();
            var thisWeekData = window.localStorage.getItem('thisWeekData')
            if(thisWeekData != null){
                indexNapiGombokMegjelenitese(JSON.parse(thisWeekData), false);
            } else{
                error();
            }
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
            window.localStorage.setItem('allWeekData', responseData)
            indexNapiGombokMegjelenitese(responseJSON, true);

        },
        error: function(jqXHR, textStatus, errorThrown) {
            error();
        }
    });
}


var clickedButton;
var url = new URL(window.location.href.replace("index.html", "egy_nap.html")); //URL query param








function egyNapAnyagai() {
    var param = new URLSearchParams(window.location.search);
    clickedButton = param.get('day');
    if (param.get('mindegyikHet') == 'true') {
        anyagokLekereseEsMegjelenitese(true);
    }
    else { // aktuális hét
        anyagokLekereseEsMegjelenitese(false);
    }
}
