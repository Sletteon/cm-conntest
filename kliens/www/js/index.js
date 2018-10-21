window.onload = function() {
    getMaterialOfThisWeek();
    getMotd();
}



// lekéri minden hét anyagát
function getAllMaterial() {
    info('Mindegyik hét mutatása');
    document.getElementById('socket').innerHTML='';
    getMaterial(getUrl(), false, function(responseData, textStatus, jqXHR) {
        responseJSON = JSON.parse(responseData);
        window.localStorage.setItem('allWeekData', responseData);
        showDays(responseJSON, true);
    });
}

// lekéri az e heti anyagot
function getMaterialOfThisWeek() {
    getMaterial(getUrl(), getWeek(), function(responseData, textStatus, jqXHR) {
        responseJSON = JSON.parse(responseData);
        window.localStorage.setItem('allWeekData', responseData);
        showDays(responseJSON, true);
    });
}



// megjeleníti a HTML-ben a kapott anyag napjait
function showDays(responseJSON, allWeek) {
    pufferedMaterial = []
    for (i = 0; i < responseJSON.length; i++) {
        pufferedMaterial.push(responseJSON[i].anyag);
    }

    pufferedDay = []
    for (i = 0; i < responseJSON.length; i++) {
        pufferedDay.push(responseJSON[i].nap);
    }

  days = pufferedDay.unique()
  days.sort()
  DayDict = {
      0: "Hétfő",
      1: "Kedd",
      2: "Szerda",
      3: "Csütörtök",
      4: "Péntek",
      5: "Szombat",
      6: "Vasárnap"
  }
  var existingDays;
  for (i = 0; i < days.length; i++) {
      existingDays = days[i];
      document.getElementById('socket').innerHTML += '<button class="btn btn-primary teljesKepernyoBootstrapPrimary" onclick="navigate(' + existingDays + ', ' + allWeek + ')">' + DayDict[existingDays] + '</button><br><br>'
  }
}

// egy nap gomjára kattintva elvezet minket az adott nap egy_nap.html-jéhez
function navigate(day, allWeek) {
    //console.log(clickedButton);
    if (allWeek) {
        url.searchParams.append('allWeek', true); //URL query param
    }
    url.searchParams.append('day', day); //URL query param
    location.href = url; //URL query param
}

// lekéri a napi üzenetet és meghívja a showMotd() függvényt az eredménnyel
// ha a legutóbbi mentett napi üzenetet már bezártuk (motdDismiss()), ne jelenítsük meg újra
function getMotd() {
    var motdDismissed = window.localStorage.getItem('motdDismissed')
    $.ajax({
        type: "get",
        url: getUrl() + "/motd",
        success: function(responseData, textStatus, jqXHR) {
            if (responseData != motdDismissed) {
                showMotd(responseData);
            }
        },

        /* ha nincs internet hozzáférés, már úgy is kiírtuk, mivel az anyagok sem töltenek be */
        error: function(jqXHR, textStatus, errorThrown) {
        }

    });
}

// megjeleníti a paraméterben megadott napi üzenetet a HTML-ben
function showMotd(message) {
    var infoAlert = document.createElement("DIV");
    infoAlert.innerHTML = '<div class="navbar navbar-fixed-bottom"><div class="alert alert-sm alert-info fade in"><a href="#" onclick="motdDismiss(\'' + message + '\')" class="close" data-dismiss="alert" aria-label="close">&times;</a>' + message + '</div></div>';
    document.getElementById('body').appendChild(infoAlert);
}

// ha bezárták a napi üzenetet, ne jelenítsük meg újra
function motdDismiss(motdMessage) {
    window.localStorage.setItem('motdDismissed', motdMessage)
}