function dates_order(before, after){
	if (before.getFullYear() < after.getFullYear())
		return true;
	if (before.getMonth() < after.getMonth())
		return true;
	if (before.getDate() <= after.getDate())
		return true;
	return false;
}


function validate(){
	start_date_s = document.getElementById('datepicker1').value
	end_date_s = document.getElementById('datepicker2').value
	text = document.getElementById('text').value

	var alert_message=''
	
	if (start_date_s == ''){
		alert_message = alert_message + '<li>Data de inceput nu e specificata</li>'
	}	
	if (end_date_s == ''){
		alert_message = alert_message + '<li>Data de final nu e specificata</li>'
	}	
	if (text == ''){
		alert_message = alert_message + '<li>Textul anuntului este gol</li>'
	}
	start_date = new Date(start_date_s)
	end_date = new Date(end_date_s)

	if (start_date.toJSON()==null || end_date.toJSON()==null){
		alert_message = alert_message + '<li>Formatul datei trebuie sa fie yyyy-mm-dd sau mm/dd/yyyy</li>'
	}
	else {
		if (!dates_order(start_date, end_date)){
			alert_message = alert_message + '<li>Data de inceput trebuie sa fie inaintea datei de final</li>'
		}
	}

	if (alert_message==''){
		return true;
	}
	
	document.getElementById('alert').innerHTML = alert_message;
	return false;
}