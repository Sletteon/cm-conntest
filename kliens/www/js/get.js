function getUrl/*ardCoded*/() {
    var IPaddress = '46.139.116.9'; /*document.getElementById("IP").value;*/
    /*var IPaddress = '46.139.116.9';*/
    var Port = 5000; /*document.getElementById("Port").value;*/

    return "http://" + IPaddress + ":" + Port;
}

function getUrls/*SoftCoded*/() {
	var IPaddress = document.getElementById("IP").value;
    /*var IPaddress = "46.139.116.9";*/
    var Port = document.getElementById("Port").value;

    return "http://" + IPaddress + ":" + Port;
}


// https://coderwall.com/p/nilaba/simple-pure-javascript-array-unique-method-with-5-lines-of-code
// Ha egy listában több ugyanolyan elem is megtalálható, csak egy ilyen elemet adjon vissza

// napok lekérésénél lehet hasznos

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



// ha kiválasztottak egy kép-fájlt

document.getElementById("getButton2").onclick = function() {
    AnyagLekeres();
};

