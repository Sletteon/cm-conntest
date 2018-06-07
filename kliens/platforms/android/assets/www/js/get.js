window.onload = function(){

    if(window.location.href.search("nap.html")){
                alert("halo")
        AnyagLekeres2();
    }
}
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

            /*document.getElementById("socket").innerHTML = '<h2>' + responseData + '<h2>';
            console.log('Első bejegyzés szerkesztője: ' + '\n' + responseJSON[0].uname + '\n -----');*/

			// Összes JSON anyaga
			pufferAnyag = []
			for (i = 0; i < responseJSON.length; i++) {
				pufferAnyag.push(responseJSON[i].anyag);
			}
			console.log('Összes JSON anyaga: ' + '\n' + pufferAnyag + '\n -----');
            /*document.getElementById("socket").innerHTML += '<h2>' + pufferAnyag + '<h2>';*/

			// Összes JSON napja
			pufferNap = []
			for (i = 0; i < responseJSON.length; i++) {
				pufferNap.push(responseJSON[i].nap);
			}
            napok = pufferNap.unique()
            napok.sort()
            DayDict={0:"Hétfő",1:"Kedd",2:"Szerda",3:"Csütörtök",4:"Péntek"}
            var adottNap
            for(i = 0; i< napok.length; i++){
                adottNap=napok[i];
                document.getElementById('socket').innerHTML += '<button class="button button2" onclick=navigate(' + adottNap + ') id= "day ' + adottNap + '">' + DayDict[adottNap] + '</button>'
            }
			// Ne az összes napot írja ki, hanem mindenből csak egyet (ha van legalább arra a napra bejegyzés)
			console.log('Összes JSON napja: ' + '\n' + pufferNap.unique() + '\n -----');

		console.log(JSON.stringify(responseJSON))
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert("Hiba a kapcsolat létesítésekor. (lásd konzol)");
        }
    });
}
function AnyagLekeres2() {
    $.ajax({
        type: "get",
        url: getUrl(),
        success: function(responseData, textStatus, jqXHR) {
			responseJSON = JSON.parse(responseData)

            for(i=0; i < responseJSON.length; i++){
        if(responseJSON[i].nap == clickedButton){
            document.getElementById("socket2").innerHTML += '<h2>Tantárgy: ' + responseJSON[i].tant + '</h2>'
            document.getElementById("socket2").innerHTML += '<h2>Anyag: ' + responseJSON[i].anyag + '</h2>'
        }
    }
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
var clickedButton;
function navigate(val){
    navigate2('nap.html')
    clickedButton = val;
}
function navigate2(val){
    location.href = val;
    write();
}