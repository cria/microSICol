function clearForm() {
	document.getElementById('txt_datetime_from').value = '';
	document.getElementById('txt_datetime_to').value = '';
	document.getElementById('cmb_user').selectedIndex = 0;
	document.getElementById('cmb_operation').selectedIndex = 0;
	document.getElementById('txt_value').value = '';
	document.getElementById('txt_record').value = '';
	document.getElementById('txt_strain_code').value = '';
	document.getElementById('txt_lot').value = '';
	document.getElementById('cmb_field').selectedIndex = 0;
	document.getElementById('txt_value').value = '';
}

function validateTraceability(dateformat)
{
	errors = false;
	
	datetime_from = document.getElementsByName('datetime_from')[0];
	datetime_to = document.getElementsByName('datetime_to')[0];
	
	if (!checkValidDate(datetime_from,null,dateformat)) errors = true;
	if (!checkValidDate(datetime_to,null,dateformat)) errors = true;
	
	//If all correct then submit
	if (!errors)
	{
	    Feedback(0);
	    document.getElementById('form_filter').submit();
	}
	else Feedback(-1);
}