window.onload = function() {
    var UName = window.localStorage.getItem("UName");
	// amennyiben nincs felhnév mentve, prompttal kérjen egyet
    if (UName == null) {
        UName = prompt("Add meg a beceneved:");
        window.localStorage.setItem("UName", UName);
    }
    // mikor betöltődik az oldal, állítsa be a mutató kurzort a
    // felhnév törléshez, és fehéret a kapcsolódás állapot szövegéhez
    document.getElementById("unameDel").style.cursor = "pointer";
    document.getElementById("connState").style.color = "white";

	// kérje le a napot, és állítsa be a nap ID-jű selectet
    var dateObj = new Date();
    var nap = dateObj.getDay();

    switch (nap) {
        case 0:
            document.getElementById("nap").value = "K";
            break;
        case 1:
            document.getElementById("nap").value = "H";
            break;
        case 2:
            document.getElementById("nap").value = "K";
            break;
        case 3:
            document.getElementById("nap").value = "S";
            break;
        case 4:
            document.getElementById("nap").value = "C";
            break;
        case 5:
            document.getElementById("nap").value = "P";
            break;
        case 6:
            document.getElementById("nap").value = "K";
            break;
    }
}

// ha az online paraméter igaz, legyen zöld a connState,
// de ha hamis, legyen piros
// ja, meg írja ki a kapcsolódási állapotot
function networkStatus(online) {
    if (online) {
        document.getElementById("connState").style.backgroundColor = "LimeGreen";
        document.getElementById("connState").innerHTML = "Online";
    }
    if (online === false) {
        document.getElementById("connState").style.backgroundColor = "red";
        document.getElementById("connState").innerHTML = "Offline";
    }
}

function objectifyForm(formArray) {
	var returnArray = {};
	for (var i = 0; i <formArray.length; i++) {
		returnArray[formArray[i]['name']] = formArray[i]['value'];
	}
	return returnArray;
}

function getUrl(){
	var IPaddress = document.getElementById("IP").value;
	var Port = document.getElementById("Port").value;

	return "http://" + IPaddress + ":" + Port
}
function receive() {
	var IPaddress = document.getElementById("IP").value;
	var Port = document.getElementById("Port").value;

	$.ajax({
		type : "get",
		url : getUrl(),
		success: function(responseData, textStatus, jqXHR) {
			document.getElementById("socket").innerHTML = responseData;
		},
		error: function(jqXHR, textStatus, errorThrown) {
			alert(errorThrown);
			console.log(errorThrown);
		}
	})
}


function getDataFromHTMLAndSendSetCommand(){

    var napSelect = document.getElementById("nap");
    var nap = napSelect.options[napSelect.selectedIndex].value;

	var hetSelect = document.getElementById("het");
    var het = hetSelect.options[hetSelect.selectedIndex].value;

	var sendingJSON = {
		"uname" : window.localStorage.getItem("UName"),
		"het" : document.getElementById("het").options[document.getElementById("het").selectedIndex].value,
		"nap" : document.getElementById("nap").options[document.getElementById("nap").selectedIndex].value,
		"tant" : document.getElementById("tantargy").value,
		"anyag" : document.getElementById("anyag").value
	};
	console.log(JSON.stringify(sendingJSON))

	$.ajax({
		type: "post",
		url: getUrl(),
		data: JSON.stringify(sendingJSON),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function(responseData, textStatus, jqXHR) {
		},
		error: function(jqXHR, textStatus, errorThrown) {
			console.log(textStatus);
			console.log(errorThrown);
		}
	})
    }
function getDataFromHTMLAndSendGetCommand(){
	var IPaddress = document.getElementById("IP").value;
    var Port = document.getElementById("Port").value;

    var UName = window.localStorage.getItem("UName");

    var hetSelect = document.getElementById("het");
    var het = hetSelect.options[hetSelect.selectedIndex].value;
	connObj = connect()
	connObj.onopen = function() {
		connObj.send(
			UName + separatorChar + 'get' + separatorChar + het + separatorChar
		);
		connObj.onmessage = function(gotMessage) {
		    networkStatus(true);

		    var gotList = [];
        	console.log(gotMessage.data);
		    gotList.push(gotMessage.data);

        	document.getElementById("socket").innerHTML = gotList;
		}
	}
}

document.getElementById("getButton").onclick = function() {
	alert("Még nincs kész.")
};
// ha megnyomják ezt a gombot, futtassa le ezt az anonim funkciót
document.getElementById("connButton").onclick = function() {
    getDataFromHTMLAndSendSetCommand();
};
// ha a gombok alatti szövegre kattintanak, törölje a felhasználónevet,
// és frissítse az oldalt
document.getElementById("unameDel").onclick = function() {
    window.localStorage.removeItem("UName");
    location.reload(false);
};
