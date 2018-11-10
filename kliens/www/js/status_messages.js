// STATUS_MESSAGES.JS - siker/hiba/figyelmeztető jellegű üzenetek függvényei

// kiüríti a státuszdobozt
function removePreviousStatus() {
    try {
        document.getElementById('statusDiv').innerHTML = '';
    } catch(err) {}
}

// sikerüzenet
function success(message, clearStatus=false) {
    if (clearStatus) {
        removePreviousStatus();
    }
    var successAlert = document.createElement("DIV");
    successAlert.innerHTML = '<div class="alert alert-sm alert-success">' + message + '</div>';
    document.getElementById('statusDiv').appendChild(successAlert);
}

// információ
function info(message, clearStatus=false) {
    if (clearStatus) {
        removePreviousStatus();
    }    var infoAlert = document.createElement("DIV");
    infoAlert.innerHTML = '<div class="alert alert-sm alert-info">' + message + '</div>';
    document.getElementById('statusDiv').appendChild(infoAlert);
}

// hibaüzenet
function error(clearStatus=false) {
    if (clearStatus) {
        removePreviousStatus();
    }    var errAlert = document.createElement("DIV");
    errAlert.innerHTML = '<div class="alert alert-sm alert-danger">Hiba történt! Biztos, hogy van neted?</div>';
    document.getElementById('statusDiv').appendChild(errAlert);
}

// 'nincs internet' jelzés
function noInternetMessage(clearStatus=false) {
    if (clearStatus) {
        removePreviousStatus();
    }    var infoAlert = document.createElement("DIV");
    infoAlert.innerHTML = '<div class="alert alert-sm alert-warning">Offline vagy. Csak a heti bejegyzéseket tudod megnézni és nem tudsz törölni.</div>';
    document.getElementById('statusDiv').appendChild(infoAlert);
}