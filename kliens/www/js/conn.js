window.onload = function() {
    var UName = window.localStorage.getItem("UName");
    // amennyiben nincs felhnév mentve, prompttal kérjen egyet
    if (UName == null) {
        UName = prompt("Add meg a beceneved:");
        window.localStorage.setItem("UName", UName);
    }

	document.getElementById("nap").value = getDay();

}

// visszaadja a mai napnak a betűkódját
function getDay() {

    var dateObj = new Date();
    var nap = dateObj.getDay();

    switch (nap) {
        case 0: // vasárnap
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
        case 6: // szombat
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

function getUrlH/*ardCoded*/() {
    var IPaddress = 'localhost'; /*document.getElementById("IP").value;*/
    var Port = 5000; /*document.getElementById("Port").value;*/

    return "http://" + IPaddress + ":" + Port;
}

function getUrl/*SoftCoded*/() {
	var IPaddress = document.getElementById("IP").value;
    var Port = document.getElementById("Port").value;

    return "http://" + IPaddress + ":" + Port;
}


// https://coderwall.com/p/nilaba/simple-pure-javascript-array-unique-method-with-5-lines-of-code
// Ha egy listában több ugyanolyan elem is megtalálható, csak egy ilyen elemet adjon vissza

// napok lekérésénél lehet hasznos
Array.prototype.unique = function() {
  return this.filter(function (value, index, self) {
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
            console.log('Első bejegyzés szerkesztője: ' + '\n' + responseJSON[0].uname + '\n -----');

			// Összes JSON anyaga
			pufferAnyag = []
			for (i = 0; i < responseJSON.length; i++) {
				pufferAnyag.push(responseJSON[i].anyag);
			}
			console.log('Összes JSON anyaga: ' + '\n' + pufferAnyag + '\n -----');

			// Összes JSON napja
			pufferNap = []
			for (i = 0; i < responseJSON.length; i++) {
				pufferNap.push(responseJSON[i].nap);
			}
			// Ne az összes napot írja ki, hanem mindenből csak egyet (ha van legalább arra a napra bejegyzés)
			console.log('Összes JSON napja: ' + '\n' + pufferNap.unique() + '\n -----');
			document.getElementById('socket').innerHTML = '<h2>Napok: </h2>' + pufferNap.unique()

		console.log(JSON.stringify(responseJSON))
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Hiba a kapcsolat létesítésekor. (lásd konzol)");
        }
    });
}

function AnyagBeallitas() {

    var napSelect = document.getElementById("nap");
    var nap = napSelect.options[napSelect.selectedIndex].value;

    // var hetSelect = document.getElementById("het");
    // var het = hetSelect.options[hetSelect.selectedIndex].value;

    var sendingJSON = {
        "uname": window.localStorage.getItem("UName"),
        "het": getWeek(),
        "nap": nap,
        "tant": document.getElementById("tantargy").value,
        "anyag": document.getElementById("anyag").value,
	"pic": getImage()
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

function BejegyzTorlese() {
    $.ajax({
        type: "delete",
        url: getUrl() + "/delete/" + document.getElementById('deleteObj').value,
        success: function(responseData, textStatus, jqXHR) {},
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Hiba a kapcsolat létesítésekor. (lásd konzol)");
        }
    });
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
	} catch(TypeError) {
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

document.getElementById("connButton").onclick = function() {
    AnyagBeallitas();
};

document.getElementById("objDelButton").onclick = function() {
	BejegyzTorlese();
};
	
// ha a gombok alatti szövegre kattintanak, törölje a felhasználónevet,
// és frissítse az oldalt
document.getElementById("unameDel").onclick = function() {
    window.localStorage.removeItem("UName");
    location.reload(false);
};
