// CONN.JS - hálózati operációk (lekérés/beküldés/törlés) függvényei

// visszaadja a mostani hét számát az évben
function getWeek() {
    Date.prototype.getWeekNumber = function() {
        var d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()))
        var dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
    };
    return new Date().getWeekNumber();
}

// visszaadja a megfelelő URL-t a hálózati operációkhoz
function getUrl() {
    var IPaddress = '46.139.116.9';
    var Port = 5000;
    return "http://" + IPaddress + ":" + Port;
}

/*  KÉPEK BEKÜLDÉSÉHEZ KELLŐ FÜGGVÉNYEK, MÉG KELLHET
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
    document.getElementById("picSelect").addEventListener("change", draw, false);

    document.getElementById("getButton").onclick = function() {
    AnyagLekeres();
    };
*/

// ha egy listában több ugyanolyan elem is megtalálható, csak egy ilyen elemet adjon vissza
Array.prototype.unique = function() {
    return this.filter(function(value, index, self) {
        return self.indexOf(value) === index;
    });
}

// GET lekérést küld a megadott URL-re
// ha a 'week' változó hamis, minden anyagot lekér
function getMaterial(url, week, successFunction) {
    if (week==false) {
        console.log('GET: ' + url + '/')
        $.ajax({
            type: "get",
            url: url,
            success: successFunction,
            error: function(jqXHR, textStatus, errorThrown) {
                error(true);
            }
        });
    } else {
        console.log('GET: ' + url + '/het/' + week)
        $.ajax({
            type: "get",
            url: url + '/het/' + week,
            success: successFunction,
            error: function(jqXHR, textStatus, errorThrown) {
                error(true);
            }
        });
    }
}

// ugyanaz, mint a getMaterial(), csak saját hibafüggvénnyel ellátva
function getMaterialCustomError(url, week, successFunction, errorFunction) {
    if (week==false) {
        console.log('GET: ' + url + '/')
        $.ajax({
            type: "get",
            url: url,
            success: successFunction,
            error: errorFunction
        });
    } else {
        console.log('GET: ' + url + '/het/' + week)
        $.ajax({
            type: "get",
            url: url + '/het/' + week,
            success: successFunction,
            error: errorFunction
        });
    }
}

// POST metódussal lekér a megadott URL-ről
function submitMaterial(url, sendingJSON, successFunction) {
    console.log('POST: ' + url + '\tsendingJSON:' + sendingJSON)
    $.ajax({
        type: "post",
        url: url,
        data: sendingJSON,
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: successFunction,
        error: function(jqXHR, textStatus, errorThrown) {
            error(true);
        }
    });
}

// beállítások menüben történő, id alapú bejegyzéstörlés
function deleteMaterial(url, materialId) {
    console.log('DELETE: ' + url + '\tmaterialId: ' + materialId)
    $.ajax({
        type: "delete",
        url: url + "/delete/" + materialId,
        success: function(responseData, textStatus, jqXHR) {
            success('A bejegyzést sikeresen törölted', true);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            error(true);
        }
    });
}