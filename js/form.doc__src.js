// This file is named "form.doc_.js" to avoid antivirus false positives
//////////////////////////////// 
// Add multi-language fields below //
////////////////////////////////
var multi_language_fields = new Array();
multi_language_fields.push("description");

var default_multi_language_fields = new Array();
default_multi_language_fields.concat(multi_language_fields);
default_multi_language_fields.push("title");
default_multi_language_fields.push("file_name");
default_multi_language_fields.push("new_file");
default_multi_language_fields.push("description");

var mapTextArea = new Object();
mapTextArea['description_*'] = 65535;

function validateDocument()
{
    errors = false;
    //Get current Form
    form = document.getElementsByName('edit')[0];
    //Get Form Fields
    code = document.getElementsByName('code')[0];
    lbl_code = getLabel('code');
    qualifier = document.getElementsByName('qualifier')[0];
    lbl_qualifier = getLabel('qualifier');
    //Clear all warnings
    resetField(code,lbl_code);
    resetField(qualifier,lbl_qualifier);
    //Check code value
    if (isEmpty(code,lbl_code)) errors = true;
    else if (!checkCode(code,lbl_code)) errors = true;
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
    if (isEmpty(qualifier,lbl_qualifier)) errors = true;
    //Get multi-language form fields
    if (isEmptyMulti('title',false)) errors = true;
    at_least_one = false;
    for(lang in langs)
    {
        file_name = document.getElementsByName('file_name_'+langs[lang])[0]; //has value when in edit mode
        new_file = document.getElementsByName('new_file_'+langs[lang])[0];
        //Labels
        lbl_new_file = getLabel('new_file');
        //Resets
        resetField(new_file,lbl_new_file);
        //Check whether all mandatory fields are filled or not
        if (new_file.value != '' || file_name.value != '') at_least_one = true;
    }
    if (!at_least_one)
    {
      errors = true;
        showError(new_file,lbl_new_file,_("Field must not be empty."));
    }
    
    if (!errors)
    {
        document.getElementById('qualifier').disabled = false;
    }
    
    return errors;
}

function changedQualifier(qualifier)
{
  /* show/hide Test Category Field */
  if (qualifier == 5) //Qualifier == "TEST"
  {
    document.getElementById('p_test_category').style.display = 'block';
  }
  else
  {
    document.getElementById('p_test_category').style.display = 'none';
  }
}

function disableLinks()
{
    disableMenu(document.getElementById('menu'), document.getElementById('active_documents'));
    disableLink(document.getElementById('active_preferences'));
    disableLink(document.getElementById('active_configuration'));
    disableLink(document.getElementById('active_utilities'));
}

function disableQualifier()
{
    if (qualifier_blocked == true)
    {
        document.getElementById('qualifier').disabled = true;
        document.getElementById('qualifier').title = qualifier_title;
        document.getElementById('label_qualifier').title = qualifier_title;
    }
}

//Add event for window.onload
addEvent(window, 'load', disableLinks);
addEvent(window, 'load', disableQualifier)
