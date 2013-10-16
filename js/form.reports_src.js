function saveReports()
{
    document.forms['formReports'].action = "./reports.save.py";
    $('#formReports')[0].submit();
}

function disableLinks()
{
    disableMenu(document.getElementById('menu'), document.getElementById('active_reports'));
    disableLink(document.getElementById('active_preferences'));
    disableLink(document.getElementById('active_configuration'));
    disableLink(document.getElementById('active_utilities'));

    $('#save_record').css('display', 'none');    

    if ($('#step').val() == 5)
    {
        document.getElementById('save_record').style.display = "";
        document.getElementById('save_submit').href = "javascript:saveReports()";
    }
}

function validateReports(step)
{
    switch(step)
    {
        case (1):
            if (document.getElementById('name_report').value == "")
            {
                showError(document.getElementById('name_report'), null, _("Field must not be empty."));
                Feedback(-1);
                return false;
            }
            else
            {
                $('#step_next').val('2');
                $('#formReports')[0].submit();
            }

            break;

        case (2):
            if ($("#select li").size() == 0 && $("#total li").size() == 0)
            {
                showError(document.getElementById('select'), document.getElementById('label_select'), _("Field must not be empty."));
                showError(document.getElementById('total'), document.getElementById('label_total'), _("Field must not be empty."));
                Feedback(-14);
                return false;
            }
            else
            {
                generate_data();
                $('#step_next').val('3');
                $('#formReports')[0].submit();
            }
        case(3):
                retValue = true;
                $("#filterDiv_0>textarea,input:text,select").each(function()
                    {                        
                        if (!$(this).is(':hidden') && !$(this).is(':disabled'))
                        {
                            var field = $(this)[0];
                            var label = $('#span_' + $(this)[0].id)[0];
			    
                            if($(this).val() == "" && ($(this).attr('allowBlank') == undefined || $(this).attr('allowBlank') == 'no'))
                            {
                                showError(field, label, _("Field must not be empty."));
                                Feedback(-1);
                                retValue = false;
                            }
                            else if($(this).attr("data_type") == "date" )
                            {
                                if (lang_code == 'en')
                                {
                                    date_format = '%m/%d/%Y';
                                }
                                else
                                {
                                    date_format = '%d/%m/%Y';
                                }
                                if(!checkValidDate(field, label, date_format, false))
                                {
                                    Feedback(-16);
                                    retValue = false;
                                }                                
                            }
                            else if($(this).attr("data_type") == "tinyint" || $(this).attr("data_type") == "integer")
                            {
                                
                                var valid = true;
                                if($(this).attr("condition") == 'in' || $(this).attr("condition") == 'not_in')
                                {
                                    var txt = field.value.split(';');
                                    for(var i = 0; i < txt.length; i++)
                                    {
                                        if(!isInteger(txt[i]))
                                        {
                                            showError(field,label,_("Only numbers are allowed for this field."));
                                            Feedback(-16);
                                            retValue = false;
                                            valid = false;
                                            break;
                                        }
                                    }
                                }
                                else
                                {
                                    if(!isInteger(field.value))
                                    {
                                        showError(field,label,_("Only numbers are allowed for this field."));
                                        Feedback(-16);
                                        retValue = false;
                                        valid = false;                                           
                                    }
                                }
                                if(valid)
                                {
                                    resetField(field, label);
                                }
                            }
                            else if($(this).attr("data_type") == "decimal_gps" )
                            {
                                if($(this).attr("condition") == 'in' || $(this).attr("condition") == 'not_in')
                                {
                                    if(!checkListGPS($('#field_' + field.id.split('_')[1]).val(),field))
                                    {
                                        showError(field,label,_("Only decimal gps format: (+/-)DD.DDDDDDDD are allowed for this field."));
                                        Feedback(-16);
                                        retValue = false;
                                    }
                                    else
                                    {
                                        resetField(field, label);
                                    }
                                }
                                else
                                {
                                    if(!checkGPS($('#field_' + field.id.split('_')[1]).val(),field))
                                    {
                                        showError(field,label,_("Only decimal gps format: (+/-)DD.DDDDDDDD are allowed for this field."));
                                        Feedback(-16);
                                        retValue = false;
                                    }
                                    else
                                    {
                                        resetField(field, label);
                                    }
                                }
                            }
                            else if($(this).attr("data_type") == "decimal" )
                            {
                                var isList = false;
                                if($(this).attr("condition") == 'in' || $(this).attr("condition") == 'not_in')
                                {
                                    isList = true;
                                }
                                if(!checkFloat(field, label, 9, 9, true, isList))
                                {
                                    showError(field,label,_("Only decimal numbers are allowed for this field."));
                                    Feedback(-16);
                                    retValue = false;
                                }
                                else
                                {
                                    resetField(field, label);
                                }
                            }
                            else
                            {
                                resetField(field, label);
                            }
                        }                        
                    })
                if(retValue == true)
                {
                    Feedback(0);
                }
                return retValue;
            break;
        
        case(4):
            if($("#allow_chart").val() == 'false' && $("#format").val() == 3)
            {
                Feedback(-15);
                return false;
            }
            else if($("#format").val() == 2 && $("#separator").val() == '')
            {
                Feedback(-17);
                showError(document.getElementById("separator"),document.getElementById("label_separator"),_("Field must not be empty."));
                return false;                
            }
            else
            {
                $('#step_next').val('5');
                $('#formReports')[0].submit();
            }
            
    }
}

//Checks whether number is float and if it respects maximum amount of integer and decimal algarisms
function isFloat(value,max_integers,max_decimals,signed)
{
	if (value.charAt(0) == '-')
	{
		if (!signed) return false;
		value = value.substring(1); //remove sign from string
	}
	num_ints = 0;
	num_decs = 0;
	dot_read = false;
	for(i=0;i < value.length;i++)
	{
		if (value.charAt(i) == '.')
		{
			if (!dot_read) dot_read = true;
			else return false; //there should not be two decimal separators
			continue;
		}
		if (!isInteger(value.charAt(i))) return false;
		if (dot_read) num_decs++;
		else num_ints++;
		if (num_ints > max_integers) return false;
		if (num_decs > max_decimals) return false;
	}
	return true;
}

function checkFloat(obj,lbl_obj,max_integers,max_decimals,signed, isList)
{
	if (lbl_obj == null) lbl_obj = getLabel(obj.id);
	if (obj.value != '')
	{
                var txt = [];
                txt = txt.concat(obj.value);
                if(isList)
                {
                    txt = obj.value.split(';');
                }
                var valid = true;
                for(var j = 0; j < txt.length; j++)
                {
                    if (!isFloat(txt[j],max_integers,max_decimals,signed))
                    {
                        warn = _("Out of format:")+' "';
                        for(i=0;i<max_integers;i++) warn += 'D';
                        warn += '.';
                        for(i=0;i<max_decimals;i++) warn += 'D';
                        warn += '" '+ _("where D = digit.");
                        if (!signed) warn += " " + _("Positive values only.");
                        valid = false;
                        showError(obj,lbl_obj,warn);
                        return false;
                    }
                }
		if(valid == true)
		{
                    resetField(obj,lbl_obj);
                    return true;
		}
	}
	else
	{
		resetField(obj,lbl_obj);
		return true;
	}
}



function ajustarAction()
{
    if (document.location.toString().indexOf('reports.edit.py') != -1)
    {
        document.forms['formReports'].action = "./reports.edit.py";
    }
}


if (document.location.toString().indexOf('reports.edit.py') != -1 ||
    document.location.toString().indexOf('reports.new.py') != -1)
{
    //Add event for window.onload
    addEvent(window, 'load', disableLinks);
    addEvent(window, 'load', ajustarAction);
}