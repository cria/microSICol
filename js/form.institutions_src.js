//////////////////////////////// 
// Add multi-language fields below //
////////////////////////////////
var multi_language_fields = new Array();
multi_language_fields.push("comments");

var default_multi_language_fields = new Array();
default_multi_language_fields.concat(multi_language_fields);
default_multi_language_fields.push("comments");

var mapTextArea = new Object();
mapTextArea['comments_*'] = 65535;
mapTextArea['address'] = 65535;
mapTextArea['phone'] = 65535;

function validateInstitutions()
{
	errors = false;
	//Get current Form
	form = document.getElementsByName('edit')[0];
	//Get Form Fields
	_name = document.getElementsByName('name')[0];
	lbl_name = getLabel('name');
	email = document.getElementsByName('email')[0];
	lbl_email = getLabel('email');
	//Clear all warnings
	resetField(_name,lbl_name);
	resetField(email,lbl_email);
	//Check whether we have a valid email or not
	if (!checkOneEmail(email,lbl_email,true)) errors = true;
	//Check whether Textareas' content is below maximum allowed length
	if (!isValidTextArea('address',65535)) errors = true;
	if (!isValidTextArea('phone',65535)) errors = true;
	//Validate multi-language fields
	langs = document.getElementById('data_langs').value;
	langs = langs.split(',');
	for (mlf in multi_language_fields)
	{
		max_size = mapTextArea[multi_language_fields[mlf]+'_*'];
		for (lang in langs)
		{
			if (!isValidTextArea(multi_language_fields[mlf]+'_'+langs[lang],max_size)) errors = true;
		}
	}
	//Check whether all mandatory fields are filled or not
	if (isEmpty(_name,lbl_name)) errors = true;
	return errors;
}

function disableLinks()
{
	disableMenu(document.getElementById('menu'), document.getElementById('active_institutions'));
	disableLink(document.getElementById('active_preferences'));
	disableLink(document.getElementById('active_configuration'));
	disableLink(document.getElementById('active_utilities'));
}

//Add event for window.onload
addEvent(window, 'load', disableLinks);
