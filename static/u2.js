

function submitData_new(targetURL,name_of_div) {
	//Marshelling into JSON
	var dataToBeSent = "{";
	if(typeof(document.forms[0]) == 'undefined' || document.forms[0] == null){
		alert("HTML form element is not defined.");
		return;
	}
	var x = document.forms[0].elements;
	for (var i = 0; i < x.length; i++) {			
		if((x[i].getAttribute("type") != null) && 
			(x[i].getAttribute("type").toLowerCase() == 'submit' || x[i].getAttribute("type").toLowerCase() == 'button')) continue;
		
		if(i > 0) dataToBeSent += ",";
		dataToBeSent += "\""+ x[i].getAttribute("name") +"\":\""+ x[i].value +"\"";
	}
	dataToBeSent += "}";
	dataToBeSent = JSON.stringify(dataToBeSent);
	
	//Sending HTTP request to server
	sendRequest_new(targetURL, dataToBeSent,name_of_div);
	
	return false;
}

function sendRequest_new(targetURL, jsonData,name_of_div){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			showOutput_new(this.responseText,name_of_div);
		} else if (this.readyState == 4){
			alert("Error occurred with status code: "+this.status);
		}
	};
	xhttp.open("POST", targetURL, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(jsonData);
	
}

function showOutput_new(output,name){		
	var division = document.getElementById(name);
	if(division === null || division == 'undefined'){			
		division = document.createElement("div");	
		division.setAttribute("id", name);	
		division.setAttribute("style", "text-align:center");
		division.style.color = "blue";	
		var element = document.getElementsByTagName("body");
		element[0].appendChild(division);
	}		
	division.innerHTML = output
}
