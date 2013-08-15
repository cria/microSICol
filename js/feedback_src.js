//Display/hide feedback on screen
function Feedback(type)
{
	var element = document.getElementById('feedback');

	d = new Date();
	minutes = d.getMinutes();
	if (minutes < 10) minutes = "0" + minutes;
	seconds = d.getSeconds();
	if (seconds < 10) seconds = "0" + seconds;
	element.style.display = 'block';
	element.className = 'feedback_error';
	switch(type)
	{
		case (-19): //Container Three with more than 14 children per node.
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("The nodes must contain the maximum of 14 children per node.");
			blink('feedback',6,'error');
			break;
		case (-18): //Container Three with different numbers of children, each node.
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("The nodes must contain the same number of children.");
			blink('feedback',6,'error');
			break;
		case (-17): // Error - CSV type Report without a separator
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Missing Separator value for CSV Report. ");
			blink('feedback',6,'error');
	 		break;
		case (-16): // Error - Chart type Report  not allowed
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Invalid value for highlighted field ");
			blink('feedback',6,'error');
	 		break;	
		case (-15): // Error - Chart type Report  not allowed
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("The Chart type can not be selected without a totalizer.");
			blink('feedback',6,'error');
	 		break;		
		case (-14): // Error - Enter the selected field or totalizer
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Enter the selected field or totalizer.");
			blink('feedback',6,'error');
	 		break;
		case (-13): // Error - Division cannot be deleted because it is in use by some strain
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Division cannot be deleted because it is in use by some strain.");
			blink('feedback',6,'error');
	 		break;
		case (-12): // Error - Please fill the pattern field with at least one #
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Pattern field need at least one #.");
			blink('feedback',6,'error');
	 		break;
		case (-11): // Error - Unknow error
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("An unknow error occurred.");
			blink('feedback',6,'error');
	 		break;
		case (-10): // Error - Access Denied on database
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Access Denied on database.");
			blink('feedback',6,'error');
	 		break;
		case (-9): // Error - Access denied for user 'sicol'@'%' to database
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Access denied for user sicol@% to database.");
			blink('feedback',6,'error');
	 		break;
		case (-8): // Error - Database has not been activated
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Database has not been activated.");
			blink('feedback',6,'error');
	 		break;
		case (-7): // Error - Could not connect to database
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Could not connect to database.");
			blink('feedback',6,'error');
			break;
		case (-6): // coll with repeated code
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Repeated code for this collection.");
			blink('feedback',6,'error');
			break;
		case (-5): // Subcoll with repeated code
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Repeated code for this Subcollection.");
			blink('feedback',6,'error');
			break;
		case (-4): // choose an test in quality
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Please, choose at least one test.");
			blink('feedback',6,'error');
			break;
		case (-3): //invalid image file
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Invalid image file.");
			blink('feedback',6,'error');
			break;
		case (-2): //permission denied to open file
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Permission denied to edit config.xml.");
			blink('feedback',6,'error');
			break;
		case (-1): //error message
			//Show client time in order to warn him that a new validation has been done.
			element.innerHTML = '['+d.getHours()+':'+minutes+':'+seconds+"] "+_("Please check all highlighted fields.");
			blink('feedback',6,'error');
			break;
		case 0: //no message
			element.style.display = 'none';
			element.className = 'feedback_ok';			
			break;
		case 1: //ok message after insert or update
			element.style.display = 'block';
			element.className = 'feedback_ok';
			element.innerHTML = _("Data inserted/updated successfully.");
			blink('feedback',6,'ok');
			break;
		case 2: //ok message after DELETE
			element.style.display = 'block';
			element.className = 'feedback_ok';
			element.innerHTML = _("Data deleted successfully.");
			blink('feedback',6,'ok');
			break;
	}
}

//Blink error message in order to call user attention
function blink(obj_id,time,type)
{
	obj = document.getElementById(obj_id);
	if (time)
	{
		time--;
		if (time % 2) obj.className = "feedback_"+type+"_blink";
		else obj.className = 'feedback_'+type;
		setTimeout("blink('"+obj_id+"',"+time+",'"+type+"')",250);
	}
	else obj.className = 'feedback_'+type;
}
