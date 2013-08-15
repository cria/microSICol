/* Global Counter used to create new IDs for dynamically generated form elements */
var global_counter = 1;

//Validate given form (may need to inform which dateformat is being used)
function validate(form_name,dateformat)
{
    errors = false;
    if (form_name == "species") errors = validateSpecies();
    else if (form_name == "doc") errors = validateDocument();
    else if (form_name == "ref") errors = validateReference();
    else if (form_name == "people") errors = validatePeople();
    else if (form_name == "institutions") errors = validateInstitutions();
    else if (form_name == "strains") errors = validateStrains(dateformat);
    else if (form_name == "distribution") errors = validateDistribution(dateformat);
    else if (form_name == "preservation") errors = validatePreservation(dateformat);
    else if (form_name == "preferences") errors = validatePreferences();
    else if (form_name == "stockmovement") errors = validateStockMovement(dateformat);
    else if (form_name == "container")
    {
        anotherError = setContainerStructure();
        errors = validateContainer(dateformat);
    }
    else
    {
        form_name = '';
    }
    
    //only will be -1 if container three was empty
    if (errors == -1)
    {
        Feedback(0); 
    }
    else
    {
        if (form_name == "container" && anotherError != "")
        {
            Feedback(anotherError);
        }
        else
        {
            //If all correct then submit
            if (!errors && (form_name != ''))
            {
                Feedback(0);
                document.forms['edit'].action = setActiveTab(document.forms['edit'].action);
                document.forms['edit'].submit();
            }
            else
            {
                Feedback(-1);
            }
        }
    }
}

//Deals with tinyMCE's onblur
function tinyMCE_onblur()
{
    sicolid = tinyMCE.selectedInstance.formTargetElementId;
    //Check whether we are dealing with a multi-language field or not
    for (mlf in multi_language_fields)
    {
        //Does it start with one of the multi_language_fields names?
        if (sicolid.indexOf(multi_language_fields[mlf]) === 0)
        {
            isValidTextArea(sicolid,mapTextArea[multi_language_fields[mlf]+'_*']);
            return true;
        }
    }
    //Validate TextArea
    isValidTextArea(sicolid,mapTextArea[sicolid]);
    return true;
}

//Validate textarea maximum length and return whether any errors occurred
function isValidTextArea(obj_name,obj_max_size)
{
    obj = document.getElementsByName(obj_name)[0];
    lbl_obj = getLabel(obj_name);
    if (lbl_obj == null) lbl_obj = getLabel(obj_name.substring(0,obj_name.lastIndexOf("_")));
    //Reset textarea colors
    resetField(obj,lbl_obj);
    obj_content = tinymce.EditorManager.get(obj_name);
    //Check maximum size restriction
    if (obj_content.length > obj_max_size)
    {
        showError(obj,lbl_obj,_("Text and HTML code exceeded maximum allowed size = ") + obj_max_size + _(". Current size = ") + obj_content.length + '.');
        return false;
    }
    return true;
}

function isEmptySelect(obj)
{
    lbl_obj = getLabel(obj.id);
    //Reset select colors
    resetField(obj,lbl_obj);
    if (obj.length == 0 || obj.selectedIndex == 0)
    {
        showError(obj,lbl_obj,_("Please, choose an option."));
        return true;
    }
    return false;
}

/* Traverse all elements recursively changing its ID coherently */
function renameFormElements(main_obj)
{
  //Visit current node
  if (main_obj.getAttribute('id') != null)
  {
    main_obj.setAttribute('id',main_obj.getAttribute('id')+'_'+global_counter);
  }
  if (main_obj.getAttribute('for') != null)
  {
    main_obj.setAttribute('for',main_obj.getAttribute('for')+'_'+global_counter);
  }
  if (main_obj.getAttribute('name') != null)
  {
    main_obj.setAttribute('name',main_obj.getAttribute('name')+'_'+global_counter);
  }
  //Fix IE-only BUG
  //Description: IE does not allow dynamically changing "name" attribute of radio buttons...
  if (main_obj.tagName.toUpperCase() == 'INPUT')
  {
    if (main_obj.type == 'radio')
    {
        //Change radiobutton for a working one
        new_obj = document.createElement('span');
        str_extra = '';
        str_extra2 = '';
        if (main_obj.name.indexOf('preservation_origin') != -1) str_extra = "onclick='changedOrigin(this)'";
        if (main_obj.checked) str_extra2 = "checked='checked'";
        new_obj.innerHTML = "<input  type='radio' "+str_extra2+" "+str_extra+" value='"+main_obj.value+"' class='radio' id='"+main_obj.id+"' name='"+main_obj.name+"' />";
        noeudParent = main_obj.parentNode;
        noeudParent.removeChild(main_obj);
        noeudParent.appendChild(new_obj);
    }
  }
  /* Traverse each child */
  for (var i=0;i < main_obj.childNodes.length; i++)
  {
      obj = main_obj.childNodes[i];
      //nodeType == 1 is Element. nodeType == 3 is TextNode (ignore it)
      if (obj.nodeType == 1) renameFormElements(obj);
  }
}

//Allow user to type numbers only
//To be used with onkeyup event
function numberOnly(obj)
{
  var numbers = "0123456789";
  var i = 0;
  var changed = false;
  for (i=0;i < obj.value.length; i++)
  {
    if (numbers.indexOf(obj.value.charAt(i)) == -1)
    {
      changed = true;
      break;
    }
  }
  if (changed)
  {
    //Remove all non-number characters
    obj.value = obj.value.replace(/\D+/,'');
  }
}

function numberOnlySlash(obj)
{
  var numbers = "0123456789/";
  var i = 0;
  var changed = false;
  for (i=0;i < obj.value.length; i++)
  {
    if (numbers.indexOf(obj.value.charAt(i)) == -1)
    {
      changed = true;
      break;
    }
  }
  if (changed)
  {
    //Remove all non-number characters
    obj.value = obj.value.replace(/\D+/,'');
  }
}

//Allow user to type numbers only
//To be used with onkeyup event
function numberOnlyGPS(obj, separator)
{
  var numbers = "0123456789" + separator;
  var i = 0;
  
  for (i=0;i < obj.value.length; i++)
  {
    if (numbers.indexOf(obj.value.charAt(i)) == -1)
    {
      obj.value = obj.value.replace(obj.value.charAt(i),'');      
    }
  }  
}

//Checks whether mandatory field is filled or not
function isEmpty(obj,lbl_obj)
{
    if (lbl_obj == null) lbl_obj = getLabel(obj.id);

    if ((obj.value == '')||(obj.value == '<br />'))
    {
        showError(obj,lbl_obj,_("Field must not be empty."));
        return true;
    }
    else
    {
        resetField(obj,lbl_obj);
        return false;
    }
}

//Checks if a field have the same value of another field
function isSameValue(obj1,lbl_obj1,obj2,lbl_obj2,msg)
{
    if (lbl_obj1 == null) lbl_obj1 = getLabel(obj1.id);
    if (lbl_obj2 == null) lbl_obj2 = getLabel(obj2.id);
    if (obj1.value != obj2.value)
    {
        showError(obj1,lbl_obj1,msg);
        showError(obj2,lbl_obj2,msg);
        return true;
    }
    else
    {
        resetField(obj1,lbl_obj1);
        resetField(obj2,lbl_obj2);
        return false;
    }
}

//Reset colors in current form field
function resetField(obj,lbl)
{
    if(obj == null) return;
    //Check whether we are dealing with a tinyMCE form field or not
    // OLD WAY: if (obj.getAttribute("convert_this") == "true") //tinyMCE form field
    if (obj.className == "mceEditor") //tinyMCE form field
    {
        _table = obj.parentNode.getElementsByTagName('table')[0];
        _table.style.borderColor = "rgb(155,176,107)"; //default color
        _table.title = '';
    }
    else
    {
        obj.style.borderColor = "rgb(155,176,107)"; //default color
        obj.title = '';
    }
    if (lbl)
  {
    lbl.style.color = "#688e23"; //default color
    lbl.title = '';
    //Clear warning icon on corresponding Tab
    tab = lbl;
    while(tab && (tab.tagName != 'DIV' || tab.className != 'data')) tab = tab.parentNode;
    
    if (tab)
    {
        tab = document.getElementById('tab_'+tab.id);
        if(tab){
            v_error = new Array();
            if (tab.getAttribute("error_labels"))
            {
                v_error = tab.getAttribute("error_labels").split(',');
                if (v_error != '')
                {
                    for(i in v_error)
                    {
                        if (v_error[i] == obj.id)
                        {
                            v_error.splice(i,1); //remove 1 element at index i
                            break;
                        }
                    }
                }
                tab.setAttribute("error_labels",v_error.toString());
            }
            else tab.setAttribute("error_labels","");
            if (tab.getElementsByTagName("img")[0] && (v_error.toString() == '')) tab.removeChild(tab.getElementsByTagName("img")[0]);
        }
    }
  }
}

//Show error colors in current form field
function showError(obj,lbl,msg)
{
    //Check whether we are dealing with a tinyMCE form field or not
    if (obj.getAttribute("convert_this") == "true") //tinyMCE form field
    {
        _table = obj.parentNode.getElementsByTagName('table')[0];
        _table.style.borderColor = "rgb(183,104,62)";
        _table.title = msg;
    }
    else
    {
        obj.style.borderColor = "rgb(183,104,62)";
        obj.title = msg;
    }

    if (lbl)
    {        
        lbl.style.color = "rgb(183,104,62)";
        lbl.title = msg;
        //Show warning icon on corresponding Tab
        tab = lbl;
        while(tab && (tab.tagName != 'DIV' || tab.className != 'data')) tab = tab.parentNode;
        
        if (tab)
        {
            tab = document.getElementById('tab_'+tab.id);
            
            if(tab)
            {
                if (tab.getAttribute("error_labels"))
                {
                    v_error = tab.getAttribute("error_labels").split(',');
                    exists = false;
                    for (i in v_error)
                    {
                        if (v_error[i] == obj.id) exists = true;
                    }
                    if (!exists)
                    {
                        v_error.push(obj.id);
                        tab.setAttribute("error_labels",v_error.toString());
                    }
                }
                else
                {
                    tab.setAttribute("error_labels",obj.id);                                     
                }
                
                if (!tab.getElementsByTagName("img")[0])
                {
                    img = document.createElement('img');
                    img.src = '../img/alert.png';
                    img.title = _("Warning Icon");
                    img.alt = _("Warning Icon");
                    tab.appendChild(img);
                }
            }
        }
    }
}

//Get corresponding label object of a given "input" object
function getLabel(fieldname)
{
  return document.getElementById('label_'+fieldname);
}

function securityChanged(sel_id)
{
   //We are only interested in changes in the "All" role option
   if (sel_id == 'perm_1')
   {
      var sel = document.getElementById(sel_id);
      val = sel.options[sel.selectedIndex].value;
      allselects = document.getElementById('all_permissions').value; //input type='hidden'
      allselects = allselects.split(',');
      if (val == 'none' || val == 'r') //Enable all other selects
      {
         for (one_sel in allselects)
         {
            //Ignore the "All"(1), "Administrator"(2), "Super-User"(3) and "Curador"(4) roles
            if (allselects[one_sel] == 1 || allselects[one_sel] == 2 || allselects[one_sel] == 3 || allselects[one_sel] == 4)
            {
                if (allselects[one_sel] == 2 || allselects[one_sel] == 3 || allselects[one_sel] == 4)
                {
                    sel = document.getElementById('perm_'+allselects[one_sel]);
                    if (sel == null) continue;
                    sel.disabled = true;
                }
                continue;
            }
            sel = document.getElementById('perm_'+allselects[one_sel]);
            if (sel == null) continue;
            sel.disabled = '';
         }
      }
      else if (val == 'w') //Disable all other selects
      {
         for (one_sel in allselects)
         {
            //Ignore the "All"(1), "Administrator"(2) and "Curador"(4) roles
            if (allselects[one_sel] == 1 || allselects[one_sel] == 2 || allselects[one_sel] == 4 || one_sel == "remove") continue;
            sel = document.getElementById('perm_'+allselects[one_sel]);
            sel.disabled = true;
         }
      }
   }
}

function isEmptyMulti(field,check_all)
{
    lbl_obj = getLabel(field);
    langs = document.getElementById('data_langs').value;
    langs = langs.split(',');
  //Only reset if field has value in all languages, else turn it all red
    if (check_all)
    {
    local_error = false;
    for(lang in langs)
    {
        obj = document.getElementsByName(field + '_' + langs[lang])[0];
        lbl_obj = getLabel(field);
        //Check whether all mandatory fields are filled or not
        obj.value = trim(obj.value);
        if (isEmpty(obj,lbl_obj)) local_error = true;
    }
  }
  //Only reset if at least one field has value, else turn it all red
  else
  {
    local_error = true;
    for(lang in langs)
    {
        obj = document.getElementsByName(field + '_' + langs[lang])[0];
        lbl_obj = getLabel(field);
        //Check whether all mandatory fields are filled or not
        obj.value = trim(obj.value);
        if (!isEmpty(obj,lbl_obj)) local_error = false;
    }
  }
    if (local_error)
    {
    for(lang in langs)
    {
        obj = document.getElementsByName(field + '_' + langs[lang])[0];
        lbl_obj = getLabel(field);
        showError(obj,lbl_obj,_("Field must not be empty in any language."));
    }
  }
  else
  {
    for(lang in langs)
    {
        obj = document.getElementsByName(field + '_' + langs[lang])[0];
        lbl_obj = getLabel(field);
        resetField(obj,lbl_obj);
    }
  }
  return local_error;
}

//Checks whether given code is whithin allowed format or not
function checkCode(obj,lbl_obj)
{
    if (lbl_obj == null) lbl_obj = getLabel(obj.id);
    if (hasSpace(obj.value))
    {
        showError(obj,lbl_obj,_("Code field must not have any spaces."));
        return false;
    }
    else if (!isAlphaNumeric(obj.value,true))
    {
        showError(obj,lbl_obj,_("Use only characters like a-z, A-Z, 0-9 or any of") + ": . - _ \\ /");
        return false;
    }
    else
    {
        resetField(obj,lbl_obj);
        return true;
    }
}

//Checks whether year has 4 digits
function ValidYear(year)
{
    if (year.length != 4) return false;
    if (!isInteger(year)) return false;
    d = new Date();
    if ((year*1) > d.getFullYear()) return false;
    return true;
}

function isInteger(s){
    var i;
    for (i = 0; i < s.length; i++)
    {
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

//Erase email if not valid and then warn the user
function checkEmailNoLabel(obj,allow_empty)
{
  valid_email = true;
    if (allow_empty)
    {
        if (obj.value != '')
        {
            if (!checkEmail(obj.value))
            {
              valid_email = false;
            }
        }
    }
    else
    {
        if (obj.value == '')
        {
              valid_email = false;
        }
        else
        {
            if (!checkEmail(obj.value))
            {
              valid_email = false;
            }
        }
    }
    if (!valid_email)
    {
    alert(_("Invalid email format."));
      obj.value = "";
      //Delete corresponding span text (if any)
      if (obj.id.indexOf('_') != -1)
      {
      split_id = obj.id.split('_');
      element_counter = split_id[split_id.length-1];
      spantxt = document.getElementById('span_email_'+element_counter);
      if (spantxt)
      {
         spantxt.innerHTML = '';
      }
    }
  }
  return valid_email;
}

function checkOneEmail(obj,lbl_obj,allow_empty)
{
    if (lbl_obj == null) lbl_obj = getLabel(obj.id);
    if (allow_empty)
    {
        if (obj.value == '')
        {
            resetField(obj,lbl_obj);
            return true;
        }
        else
        {
            if (!checkEmail(encodeURI(obj.value)))
            {
                showError(obj,lbl_obj,_("Invalid email format."));
                return false;
            }
            else
            {
                resetField(obj,lbl_obj);
                return true;
            }
        }
    }
    else
    {
        if (obj.value == '')
        {
            showError(obj,lbl_obj,_("Invalid email format."));
            return false;
        }
        else
        {
            if (!checkEmail(encodeURI(obj.value)))
            {
                showError(obj,lbl_obj,_("Invalid email format."));
                return false;
            }
            else
            {
                resetField(obj,lbl_obj);
                return true;
            }
        }
    }
}

function checkOneURL(obj, lbl_obj, allow_empty)
{
    if (lbl_obj == null)
    {
        lbl_obj = getLabel(obj.id);
    }

    if (allow_empty)
    {
        if (obj.value == '')
        {
            resetField(obj,lbl_obj);
            return true;
        }
        else
        {
            if (!checkURL(obj.value))
            {
                showError(obj,lbl_obj,_("Invalid URL format."));
                return false;
            }
            else
            {
                resetField(obj,lbl_obj);
                return true;
            }
        }
    }
    else
    {
        if (obj.value == '')
        {
            showError(obj,lbl_obj,_("Invalid URL format."));
            return false;
        }
        else
        {
            if (!checkURL(obj.value))
            {
                showError(obj,lbl_obj,_("Invalid URL format."));
                return false;
            }
            else
            {
                resetField(obj,lbl_obj);
                return true;
            }
        }
    }
}

function checkURL(strURL)
{
	for (var x = 0; x < strURL.length; x++)
	{
		if (encodeURI(strURL.substring(x, x+1)) == "%20")
		{
			return false;
		}
	}
	
    if (!hasSpace(strURL))
    {
        var validator = new RegExp();

        if (strURL.indexOf("?") == -1)
        {
            validator.compile("^((http|https)://)?[A-Za-z0-9-_]+[.][A-Za-z0-9-_]+[.][A-Za-z0-9-_]+[A-Za-z0-9-_.,/#%]*[^.,%]$");

          if (validator.test(strURL))
            {
                return true;
            }
            else
            {
            return false;
          }
        }
        else
        {
            var URLforDNS;
            var URLforGet;

            strURL = strURL.split("?");

            URLforDNS = strURL[0];
            URLforGet = strURL[1];

            validator.compile("^((http|https)://)?[A-Za-z0-9-_]+[.][A-Za-z0-9-_]+[.][A-Za-z0-9-_]+[A-Za-z0-9-_.,/%]*[^.,%]$");

            if (validator.test(URLforDNS))
            {
                if (URLforGet != '')
                {
                    validator.compile("^[A-Za-z0-9-_.,&%#+]+");

                    if (validator.test(URLforGet))
                    {
                        return true;
                    }
                    else
                    {
                        return false;
                    }
                }
                else
                {
                    return true;
                }
            }
            else
            {
                return false;
            }
        }
    }
    else
    {
        return false;
    }
}

//Prevent user to type non-alphanumeric characters
//To be used with: onkeyup events
function formatAlphaNumeric(obj,allow_special)
{
    if (allow_special) alphanum = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_./\\";
    else alphanum = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var i = 0;
  var invalid = false;
  for (i=0;i < obj.value.length; i++)
  {
     if (alphanum.indexOf(obj.value.charAt(i)) == -1)
     {
        obj.value = obj.value.replace(obj.value.charAt(i), '');
         invalid = true;         
     }
  }  
}

//Checks whether string has only alphanumeric characters or not
function isAlphaNumeric(str,allow_special)
{
    if (allow_special) alphanum = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_./\\";
    else alphanum = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var i = 0;
    for(i=0;i < str.length;i++)
    {
        if (alphanum.indexOf(str.charAt(i)) == -1) return false;
    }
    return true;
}

//Checks whether string has any space or not
function hasSpace(str)
{
    if (typeof(str) != 'string') return false;
    if (str == null || str.length == 0) return false;
    if (str.indexOf(' ') != -1) return true;
    return false;
}

function changeLanguageTab(field, par_lang){
    langs = document.getElementById('data_langs').value;
    langs = langs.split(',');
    for(lang=0; lang < langs.length; lang++)
    {
        field_current = document.getElementById(field+"_field_"+langs[lang]);
            tab_current = document.getElementById(field+"_tab_"+langs[lang]);
            var _class;

            if(langs[lang] == par_lang)
            {
                field_current.style.display = 'block';
                tab_current.className = 'active';
                if(field == 'file_name')
                {
                    file_field_current = document.getElementById("new_file_field_"+langs[lang]);
                    file_tab_current = document.getElementById("new_file_tab_"+langs[lang]);
                    file_field_current.style.display = 'block';
                }
            }
        else
        {
            field_current.style.display = 'none';
            tab_current.className = 'inactive';
            if(field == 'file_name')
            {
                file_field_current = document.getElementById("new_file_field_"+langs[lang]);
                file_tab_current = document.getElementById("new_file_tab_"+langs[lang]);
                file_field_current.style.display = 'none';
            }
        }
    }
}
/*
 ===============================CHECK EMAIL MODULE==============================================
Usage example:
    var myForm = document.imageForm
    var eField = myForm.email
    if(checkEmail(eField) != false)
    {
        myForm.submit()
    }
 ==================================================================================================
 Source: http://jennifermadden.com/javascript/emailValidation.html
*/

function checkEmail(emField)
{ //reference to email field passed as argument
    var fieldValue = emField; // store field's entire value in variable
    // Begin Valid Email Address Tests
    //if field is not empty
    if (fieldValue != "")
    {
        var atSymbol = 0;
        //loop through field value string
        for(var a = 0; a < fieldValue.length; a++)
        {
            //look for @ symbol and for each @ found, increment atSymbol variable by 1
            if(fieldValue.charAt(a) == "@")
            {
                atSymbol++;
            }
        }
        // if more than 1 @ symbol exists
        if(atSymbol > 1)
        {
            // then cancel and don't submit form
            //alert("Please Enter A Valid Email Address")
            return false;
        }
        // if 1 @ symbol was found, and it is not the 1st character in string
        if(atSymbol == 1 && fieldValue.charAt(0) != "@")
        {
			//verify if there is blank characters in the fieldValue (the JavaScript function encodes space as %20, so %20 = ' ')
			for (var x = 0; x < fieldValue.length; x++)
			{
				if (fieldValue.substring(x-1, x+2) == "%20")
				{
					return false;
				}
			}
            //look for period at 2nd character after @ symbol
            var period = fieldValue.indexOf(".",fieldValue.indexOf("@")+2);
            // "." immediately following 1st "." ?
            var twoPeriods = (fieldValue.charAt((period+1)) == ".") ? true : false;
            //if period was not found OR 2 periods together OR field contains less than 5 characters OR period is in last position
            if(period == -1 || twoPeriods || fieldValue.length < period + 2 || fieldValue.charAt(fieldValue.length-1)==".")
            {
                // then cancel and don't submit form
                //alert("Please Enter A Valid Email Address")
                return false;
            }
        }
        // no @ symbol exists or it is in position 0 (the first character of the field)
        else
        {
            // then cancel and don't submit form
            //alert("Please Enter A Valid Email Address")
            return false;
        }
    }
    // if field is empty
    else
    {
        // then cancel and don't submit form
        //alert("Please Enter A Valid Email Address")
        return false;
    }
    //all tests passed, submit form
    //alert("VALID EMAIL ADDRESS!")
    return true;
}
/* ================================ END OF CHECK EMAIL MODULE =============================== */

/*
 ================================CHECK DATE MODULE==============================================
 * DHTML date validation script for dd/mm/yyyy. Courtesy of SmartWebby.com (http://www.smartwebby.com/dhtml/)
 * Modified by Renato Arnellas Coelho 2006
 ==================================================================================================
*/
// Declaring valid date character, minimum year and maximum year
var defaultSlash= "/"; //default Slash character
var minYear=1;
___data_atual___ = new Date();
var maxYear=___data_atual___.getFullYear();

function stripCharsInBag(s, bag){
    var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++)
    {
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function daysInFebruary (year){
// February has 29 days in any year evenly divisible by four,
// EXCEPT for centurial years which are not also divisible by 400.
    return (((year % 4 == 0) && ( (!(year % 100 == 0)) || (year % 400 == 0))) ? 29 : 28 );
}

function DaysArray(n) {
  var MonthArray = new Array();
    for (var i = 1; i <= n; i++)
    {
        MonthArray[i] = 31;
        if (i==4 || i==6 || i==9 || i==11) {MonthArray[i] = 30};
        if (i==2) {MonthArray[i] = 29};
    }
    return MonthArray;
}

function isDate(dtStr, verifyRange) {
    var ret = { valid: false };

    var daysInMonth = DaysArray(12);
    var pos1=dtStr.indexOf(defaultSlash);
    var pos2=dtStr.indexOf(defaultSlash,pos1+1);
    var strDay=dtStr.substring(0,pos1);
    var strMonth=dtStr.substring(pos1+1,pos2);
    var strYear=dtStr.substring(pos2+1);
    strYr=strYear;
    if (strDay.charAt(0)=="0" && strDay.length>1) strDay=strDay.substring(1);
    if (strMonth.charAt(0)=="0" && strMonth.length>1) strMonth=strMonth.substring(1);
    for (var i = 1; i <= 3; i++)
    {
        if (strYr.charAt(0)=="0" && strYr.length>1) strYr=strYr.substring(1);
    }
    month=parseInt(strMonth);
    day=parseInt(strDay);
    year=parseInt(strYr);
    if (pos1==-1 || pos2==-1){
//      alert("The date format should be : dd/mm/yyyy")
        ret.reason = _("The date format should be dd/mm/yyyy");
        return ret;
    }
    if (strMonth.length<1 || month<1 || month>12){
//      alert("Please enter a valid month")
        ret.reason = _("Please enter a valid month");
        return ret;
    }
    if (strDay.length<1 || day<1 || day>31 || (month==2 && day>daysInFebruary(year)) || day > daysInMonth[month]){
//      alert("Please enter a valid day")
        ret.reason = _("Please enter a valid day");
        return ret;
    }
    if (strYear.length != 4 || year==0 || year<minYear || year>maxYear){
//      alert("Please enter a valid 4 digit year between "+minYear+" and "+maxYear)
        ret.reason = _("Please enter a valid 4 digit year no greater than ")+maxYear;
        return ret;
    }
    if (dtStr.indexOf(defaultSlash,pos2+1)!=-1 || isInteger(stripCharsInBag(dtStr, defaultSlash))==false){
//      alert("Please enter a valid date")
        ret.reason = _("Please enter a valid date");
        return ret;
    }
  
  if (verifyRange)
  {
        /* Date must be lesser than or equal to current date */
        date_start = day+defaultSlash+month+defaultSlash+year;
        date_end = ___data_atual___.getDate()+defaultSlash+(___data_atual___.getMonth()+1)+defaultSlash+___data_atual___.getFullYear();
        if (checkStartEnd(date_start, date_end))
        {
            ret.valid = true;
            ret.reason = 0;
            return ret;
        }
        else
        {
            ret.reason = _("Please enter a date no greater than ")+date_end;
            return ret;
        }
  }
  else
  {
        ret.valid = true;
        ret.reason = 0;
        return ret;    
  }

}

//function isDate(dtStr){
//  var obj = isDateNew(dtStr);
//  return obj.result;
//}

//Receives date in format dd/mm/yyyy and returns number whose value is yyyymmdd
function DateToNumber(date)
{
    //Format d/m/yyyy to dd/mm/yyyy
  var date_num = 0;
    var num_bars = 0;
    var day = 0;
    var missing_day_slot = false;
    var month = 0;
    var missing_month_slot = false;
    var index = 0; // auxiliar index
    var year = 0;
  for (i=0;i<date.length;i++)
    {
        if (date.charAt(i) == "/")
        {
            if (num_bars == 0) //get day
            {
                day = date.substring(0,i);
          if (i != 2) missing_day_slot = true;
            }
            if (num_bars == 1) //get month
            {
                index = 3; //in theory
                if (missing_day_slot) index = 2;
                month = date.substring(index,i);
                if ((i - index) != 2) missing_month_slot = true;
            }
            num_bars++;
        }
        if (num_bars == 2) //get year
        {
            year = date.substr(i+1,4);
            break; //exit loop
        }
    }
  date_num = year * 10000; //cast to integer and shift it to the right place
    date_num += month * 100; //cast to integer and shift it to the right place
  date_num += day * 1; //cast to integer and shift it to the right place
    return date_num;
}

//Compare two dates (start,end) and return whether they are valid
//End >= Start (returns true else returns false )
function checkStartEnd(start,end)
{
    //Change dd/mm/yyyy to yyyymmdd in order to make comparison
    start_num = DateToNumber(start);
    end_num = DateToNumber(end);
    if (start_num > end_num) return false;
    else return true;
}
/* ================================ END OF CHECK DATE MODULE =============================== */

//Checks date format
function checkValidDate(obj,lbl_obj,dateformat, verifyRange)
{
    if (lbl_obj == null)
    {
        if(obj != null)
            lbl_obj = getLabel(obj.id);
    }
    if (obj != null && obj.value != '')
    {
        var dateRet = {valid: false};
        
        var res = true;
        
        if (verifyRange == undefined)
        {
            verifyRange = true;
        }

        var list = obj.value.split(';');
        var txt = '';
        
        for(k = 0; k < list.length; k++)
        {
            var tmp = new String(list[k]);
            dateRet = isValidDate(tmp, dateformat, verifyRange);    
            // date is valid
            if (dateRet.valid) {
                resetField(obj,lbl_obj);
                //Format date according to dateformat
                aux_value = tmp.replace(/[-.]/g,'/');
                v_aux = aux_value.split('/');
                //Get the YEAR index
                if (dateformat.charAt(1) == 'Y') y_index = 0;
                else if (dateformat.charAt(4) == 'Y') y_index = 1;
                else y_index = 2;
                if (v_aux[y_index].length == 2 || v_aux[y_index].length == 1) //turn 1 or 2-digit year into 4-digit year
                {
                    v_aux[y_index] *= 1;
                    v_aux[y_index] += (v_aux[y_index] <= (new Date().getYear()-100)) ?  2000 : 1900; //getYear() returns value=(currentYear-1900)
                    v_aux[y_index] = v_aux[y_index].toString();
                }
                tmp = v_aux[0] + '/' + v_aux[1] + '/' + v_aux[2];
                if(txt != '')
                {
                    txt+=';';
                }
                txt+= tmp;
            }
            else{
                showError(obj,lbl_obj,dateRet.reason);
                return false;
            }
        }
        obj.value = txt;
        return res;
    }
    else
    {
        resetField(obj,lbl_obj);
        return true;
    }
}

function $date(date, dateformat)
{
    //Valid formats: %1/%2/%3 where 1,2,3 can be %d for day, %m for month and %Y for year
    //Parse format string
    day_ind = 0;
    month_ind = 0;
    year_ind = 0;
    format_ind = new Array(3);
    format_ind[0] = dateformat.charAt(1);
    format_ind[1] = dateformat.charAt(4);
    format_ind[2] = dateformat.charAt(7);
    if (format_ind[0] == 'd') day_ind = format_ind[0];
    if (format_ind[0] == 'm') day_ind = format_ind[0];
    if (format_ind[0] == 'Y') day_ind = format_ind[0];
    if (format_ind[1] == 'd') month_ind = format_ind[1];
    if (format_ind[1] == 'm') month_ind = format_ind[1];
    if (format_ind[1] == 'Y') month_ind = format_ind[1];
    if (format_ind[2] == 'd') year_ind = format_ind[2];
    if (format_ind[2] == 'm') year_ind = format_ind[2];
    if (format_ind[2] == 'Y') year_ind = format_ind[2];
    if (day_ind == 0 || month_ind == 0 || year_ind == 0) return false;
    //Create date in format dd/mm/yyyy
    aux_str = '';
    grab = 0;
    date_day = '';
    date_month = '';
    date_year = '';    
    
    for(i=0;i < date.length;i++)
    {
        this_char = date.charAt(i);
        if (format_ind[grab] == 'd')
        {
            if ((this_char == '/') || (this_char == '-') || (this_char == '.'))
            {
                grab++;
                date_day = aux_str;
                aux_str = '';
            }
            else aux_str += date.charAt(i);
        }
        else if (format_ind[grab] == 'm')
        {
            if ((this_char == '/') || (this_char == '-') || (this_char == '.'))
            {
                grab++;
                date_month = aux_str;
                aux_str = '';
            }
            else aux_str += date.charAt(i);
        }
        else if (format_ind[grab] == 'Y')
        {
            aux_str += date.charAt(i);
        }
    }
    date_year = aux_str;
    if (date_year.length == 2 || date_year.length == 1) //turn 1 or 2-digit year into 4-digit year
    {
      date_year *= 1;
      date_year += (date_year <= (new Date().getYear()-100)) ?  2000 : 1900; //getYear() returns value=(currentYear-1900)
      date_year = date_year.toString();
  }
    if (date_day == '' || date_month == '' || date_year == '') return false;
    return {"day":date_day, "month":date_month , "year":date_year};
}

function createDate(date, dateformat)
{
    var _date = $date(date, dateformat);
    return new Date(_date['year'] , _date['month'], _date['day']);
}

//Validate given date
function isValidDate(date,dateformat, verifyRange)
{
    //test value using the standard slash = '/'
    var _date = $date(date,dateformat);    
    return isDate(_date['day'] + defaultSlash + _date['month'] + defaultSlash + _date['year']);
}

function checkLowerDate(obj1, obj2, dateformat)
{
    if (checkValidDate(obj1, null, dateformat) && checkValidDate(obj2, null, dateformat))
    {
        if (obj1.value != "" && obj2.value != "")
        {
            if (createDate(obj1.value, dateformat) <= createDate(obj2.value, dateformat))
            {
                resetField(obj2, getLabel(obj2.id));
                return true;
            }
            else
            {
                showError(obj2,getLabel(obj2.id),_("Date out of limit."));
                return false;
            }
        }
        else
        {
            resetField(obj2, getLabel(obj2.id));
            return true;
        }
    }
    else
    {
        return false;
    }
}

function checkUpperDate(obj1, obj2, dateformat)
{
    if (checkValidDate(obj1, null, dateformat) && checkValidDate(obj2, null, dateformat))
    {
        if (obj1.value != "" && obj2.value != "")
        {
            if (Date.parse(obj1.value) >= Date.parse(obj2.value))
            {
                resetField(obj2, getLabel(obj2.id));
                return true;
            }
            else
            {
                showError(obj2,getLabel(obj2.id),_("Date out of limit."));
                return false;
            }
        }
        else
        {
            resetField(obj2, getLabel(obj2.id));
            return true;
        }
    }
    else
    {
        return false;
    }
}

/*
 ===============================AUTOMATIC DATE FORMAT MODULE==============================================
All the events below must appear together:
onkeyup="checkCharModifier(this,event)" onkeydown="return filterChar(event)" onkeypress="return checkDateSlash(this,event)" onblur="checkValidDate(this,null,'%(date_format)s')"
*/
//Save global date field value in order to avoid automatic text-cursor positioning in IE and to do some verifications
var __lastDate = '';
var __lastDate_id = ''; //don't mix different date inputs!
var __shift = false;
//onkeyup="checkCharModifier(this,event)"
function checkCharModifier(field,e, isList)
{
    var charCode=0;
    if (!e) var e = window.event;
    if (e.keyCode) charCode = e.keyCode;
    else if (e.which) charCode = e.which;
    if (charCode == 16) __shift = false;
    
    var tmp = field.value;
    if(isList)
    {
        var vet = field.value.split(';');
        tmp = vet[vet.length - 1];
    }
    //Checks how many slashes we already have
    var strDateTest = tmp;
    var firstSlash = '';
    var secondSlash = '';
    num_slashes = 0;
    ind1 = strDateTest.indexOf("/");
    ind2 = strDateTest.indexOf("-");
    ind3 = strDateTest.indexOf(".");
    if (ind1 == -1)
    {
       if (ind2 == -1)
       {
           if (ind3 != -1)
           {
             num_slashes++;
             firstSlash = '.';
             ind3 = strDateTest.indexOf(".",ind3+1);
             if (ind3 != -1)
             {
               num_slashes++;
               secondSlash = '.';
           }
         }
     }
     else
     {
         num_slashes++;
         if (ind3 != -1)
         {
            num_slashes++;
            if (ind3 < ind2)
            {
               firstSlash = '.';
               secondSlash = '-';
            }
            else
            {
               firstSlash = '-';
               secondSlash = '.';
            }
         }
         else
         {
            firstSlash = '-';
            ind2 = strDateTest.indexOf("-",ind2+1);
            if (ind2 != -1)
            {
              num_slashes++;
              secondSlash = '-';
            }
         }
     }
  }
  else
  {
     num_slashes++;
     if (ind3 != -1)
     {
        num_slashes++;
        if (ind3 < ind1)
        {
           firstSlash = '.';
           secondSlash = '/';
        }
        else
        {
           firstSlash = '/';
           secondSlash = '.';
        }
     }
     else if(ind2 != -1)
     {
        num_slashes++;
        if (ind2 < ind1)
        {
           firstSlash = '-';
           secondSlash = '/';
        }
        else
        {
           firstSlash = '/';
           secondSlash = '-';
        }
     }
     else
     {
        firstSlash = '/';
        ind1 = strDateTest.indexOf("/",ind1+1);
        if (ind1 != -1)
        {
          num_slashes++;
          secondSlash = '/';
        }
     }
  }
    //Check if we need to rollback field value
    if (num_slashes == 0)
    {
        if (strDateTest.length > 2) field.value = __lastDate;
    }
    else if (num_slashes == 1)
    {
        v_content = strDateTest.split(firstSlash);
        if (v_content[0].length > 2 || v_content[0].length == 0) field.value = __lastDate;
        else if (v_content[1].length > 2) field.value = __lastDate;
    }
    else if (num_slashes == 2)
    {
      if (firstSlash == secondSlash)
      {
        v_content = strDateTest.split(firstSlash);
        if (v_content[0].length > 2 || v_content[0].length == 0) field.value = __lastDate;
        else if (v_content[1].length > 2 || v_content[1].length == 0) field.value = __lastDate;
        else if (v_content[2].length > 4) field.value = __lastDate;
    }
    else
    {
        aux1 = strDateTest.split(secondSlash);
        aux2 = aux1[0].split(firstSlash);
        v_content = new Array(aux2[0],aux2[1],aux1[1]);
        if (v_content[0].length > 2 || v_content[0].length == 0) field.value = __lastDate;
        else if (v_content[1].length > 2 || v_content[1].length == 0) field.value = __lastDate;
        else if (v_content[2].length > 4) field.value = __lastDate;
    }
    }
    //Update last field value
    __lastDate = field.value;
    __lastDate_id = field.id;
}

//onkeydown="return filterChar(event)"
function filterChar(e)
{
    //Javascript debug functions:
    //String.fromCharCode(0x30); //returns char
    //String.charCodeAt('A'); //returns int

    var charCode=0;
    if (!e) var e = window.event;
    if (e.keyCode) charCode = e.keyCode;
    else if (e.which) charCode = e.which;
    if (charCode == 16) __shift = true;
    //Eliminate ambiguos characters
    validchars = new Array();
    validchars.push(48); //0
    validchars.push(49); //1
    validchars.push(50); //2
    validchars.push(51); //3
    validchars.push(52); //4
    validchars.push(53); //5
    validchars.push(54); //6
    validchars.push(55); //7
    validchars.push(56); //8
    validchars.push(57); //9
    validchars.push(96); //0(from numpad)
    validchars.push(97); //1(from numpad)
    validchars.push(98); //2(from numpad)
    validchars.push(99); //3(from numpad)
    validchars.push(100); //4(from numpad)
    validchars.push(101); //5(from numpad)
    validchars.push(102); //6(from numpad)
    validchars.push(103); //7(from numpad)
    validchars.push(104); //8(from numpad)
    validchars.push(105); //9(from numpad)
    validchars.push(37); //left arrow
    validchars.push(39); //right arrow
    validchars.push(8); //backspace
    validchars.push(9); //Tab
    validchars.push(46); //delete
    validchars.push(193); //'/'
    validchars.push(111); // '/' (from numpad)
    validchars.push(116); // 'F5'
    validchars.push(36); // Home
    validchars.push(35); // End
    validchars.push(109); //'-'
    validchars.push(190); //'.'
    validchars.push(194); //'.' (from numpad)
    //Ignore invalid characters
    validcode = false;
    for(number in validchars)
    {
        if (charCode == validchars[number])
        {
            validcode = true;
        }
    }
    if (!validcode) return false;
}

//onkeypress="return checkDateSlash(this,event)"
function checkDateSlash(field,e, isList)
{
    /* find out which key has been pressed */
    var charCode=0;
    if (!e) var e = window.event;
    if (e.keyCode) charCode = e.keyCode;
    else if (e.which) charCode = e.which;
    if (field.id != __lastDate_id)
    {
        __lastDate = '';
        __lastDate_id = '';
    }
    //Block invalid chars
  if (charCode > 31 && (charCode < 45 || charCode > 57))
    {
        //Do nothing if we are using control characters
        if (!(charCode == 111 || charCode == 193 || charCode == 116 || charCode == 37 || charCode == 39 || charCode == 8 || charCode == 46 || charCode == 36 || charCode == 35)) return false;
    }
    //Block invalid shifted chars
    if (charCode == 35 || charCode == 36 || charCode == 37) return false;
    
    var tmp = field.value;
    var list = '';
    if(isList)
    {
        
        var vet = field.value.split(';');
        for(i = 0; i < vet.length - 1; i++)
        {
            if(list != '')
            {
                list+= ';';
            }
            list+= vet[i];
        }
        
        tmp = vet[vet.length - 1];
    }
    //Checks how many slashes we already have
    var strDateTest = tmp;
    var firstSlash = '';
    var secondSlash = '';
    num_slashes = 0;
    ind1 = strDateTest.indexOf("/");
    ind2 = strDateTest.indexOf("-");
    ind3 = strDateTest.indexOf(".");
    if (ind1 == -1)
    {
       if (ind2 == -1)
       {
           if (ind3 != -1)
           {
             num_slashes++;
             firstSlash = '.';
             ind3 = strDateTest.indexOf(".",ind3+1);
             if (ind3 != -1)
             {
               num_slashes++;
               secondSlash = '.';
           }
         }
     }
     else
     {
         num_slashes++;
         if (ind3 != -1)
         {
            num_slashes++;
            if (ind3 < ind2)
            {
               firstSlash = '.';
               secondSlash = '-';
            }
            else
            {
               firstSlash = '-';
               secondSlash = '.';
            }
         }
         else
         {
            firstSlash = '-';
            ind2 = strDateTest.indexOf("-",ind2+1);
            if (ind2 != -1)
            {
              num_slashes++;
              secondSlash = '-';
            }
         }
     }
  }
  else
  {
     num_slashes++;
     if (ind3 != -1)
     {
        num_slashes++;
        if (ind3 < ind1)
        {
           firstSlash = '.';
           secondSlash = '/';
        }
        else
        {
           firstSlash = '/';
           secondSlash = '.';
        }
     }
     else if(ind2 != -1)
     {
        num_slashes++;
        if (ind2 < ind1)
        {
           firstSlash = '-';
           secondSlash = '/';
        }
        else
        {
           firstSlash = '/';
           secondSlash = '-';
        }
     }
     else
     {
        firstSlash = '/';
        ind1 = strDateTest.indexOf("/",ind1+1);
        if (ind1 != -1)
        {
          num_slashes++;
          secondSlash = '/';
        }
     }
  }
    if ((String.fromCharCode(charCode) == '/') || (String.fromCharCode(charCode) == '.') || (String.fromCharCode(charCode) == '-'))
    {
        //Ignore exceeding slash
        if (num_slashes == 2) return false;
        if (num_slashes == 1) //cannot have two "slashes" together
        {
            v_content = strDateTest.split(firstSlash);
            if (v_content[1].length == 0) return false;
        }
        else if (num_slashes == 0)
        {
            if (strDateTest.length == 0) return false;
        }
    }
    else //user pressed a number
    {
        numbers = "0123456789";
        if (num_slashes == 2)
        {
            if (firstSlash == secondSlash)
            {
                v_content = strDateTest.split(firstSlash);
                if (v_content[2].length > 4 && (numbers.indexOf(String.fromCharCode(charCode)) != -1) ) return false; //ignore user edit
                else if(isList && v_content[2].length == 4 && (numbers.indexOf(String.fromCharCode(charCode)) != -1) )
                {
                    field.value = strDateTest + ';';
                }
            }
            else
            {
                  v_content = strDateTest.split(secondSlash);
                  if (v_content[1].length > 4 && (numbers.indexOf(String.fromCharCode(charCode)) != -1) ) return false; //ignore user edit
            }
        }
        if (num_slashes == 1)
        {
            v_content = strDateTest.split(firstSlash);
            if (v_content[1].length > 2 && (numbers.indexOf(String.fromCharCode(charCode)) != -1) ) return false; //ignore user edit
            if (v_content[1].length == 2 && charCode != 8)
            {
                var txt = strDateTest + firstSlash;
                if(isList && list.length > 0)
                {
                    txt = list + ';' + txt;
                }                
                field.value = txt;
            }
        }
        else if (num_slashes == 0)
        {
            if (strDateTest.length > 2 && (numbers.indexOf(String.fromCharCode(charCode)) != -1) ) return false; //ignore user edit
            if (strDateTest.length == 2 && charCode != 8)
            {
                var txt = strDateTest + '/';
                if(isList && list.length > 0)
                {
                    txt = list + ';' + txt;
                }                
                field.value = txt;                
            }
        }
    }
    return true;
}
/* ================================ END OF AUTOMATIC DATE FORMAT  MODULE =============================== */

function showOnlyDefaultFieldTabs(){
    langs = document.getElementById('data_langs');
    if (langs == null) return;
    langs = langs.value.split(',');

    if (default_multi_language_fields == null || default_multi_language_fields == undefined)
    return;

    for(field in default_multi_language_fields){
        for(lang in langs){
            field_current = document.getElementById(default_multi_language_fields[field]+"_field_"+langs[lang]);
            if (field_current == null || field_current == undefined)
        continue;

            if (lang == 0){
                field_current.className = 'block';
            }else{
                field_current.className = 'none';
            }
        }
    }
}

addEvent(window, 'load', showOnlyDefaultFieldTabs);

function password_strength(input_field,output_img)
{
    input_value = document.getElementById(input_field).value;

    pattern1 = /[a-z]/; // Worth 5 points
    pattern2 = /[A-Z]/; // Worth 9 points
    pattern3 = /[-!@#$%&*()_+=.]/; // Worth 10 points
    pattern4 = /[0-9]/; // Worth 7 poinst

    points = 0;
    pattern1.exec(input_value) ? points +=  5 : points;
    pattern2.exec(input_value) ? points +=  9 : points;
    pattern3.exec(input_value) ? points += 10 : points;
    pattern4.exec(input_value) ? points +=  7 : points;
    points += input_value.length/2.;

    // If the input lenght is too short we need to penalize the points
    if (input_value.length < 5)
    {
        points = points/3.;
    }

    // Normalize the points
    if (points > 30)
    {
        strength = "pwdbar4";
    }
    else if(points > 20)
    {
        strength = "pwdbar3";
    }
    else if(points > 10)
    {
        strength = "pwdbar2";
    }
    else if(points > 0)
    {
        strength = "pwdbar1";
    }
    else if (points == 0)
    {
        strength = "pwdbar0";
    }

    // Put the result in the output div
    document.getElementById(output_img).src = '../img/' + strength + '.png';
}

function checkGPS(gps_type,obj, manual_type)
{
    return auxCheckGPS(gps_type,obj, obj.value, manual_type);    
}

function checkListGPS(gps_type,obj, manual_type)
{
    txt = obj.value.split(';');
    var i = 0;
    var valid = true;
    while(valid){
        valid = auxCheckGPS(gps_type,obj, txt[i], manual_type, true);
        i++;
    }    
    return valid;
}

function auxCheckGPS(gps_type,obj, value, manual_type, isList)
{
    //Regexp created with the help of: http://www.rexv.org/
    var dmsPattern = /^([-+]?)(\d{1,3})([^-0-9+])((\d{1,2})(\.\d+)?['`]((\d{1,2})(\.\d+)?("|''|``))?)?([NSEWnsew])?$/;
    var decPattern = /^([-+])?(\d{1,3})([.,](\d+)?)?$/;
    var lbl_obj = getLabel(obj.id);    
    //First of all, trim all spaces
    value = value.replace(/\s+/g,'');
    if (value != '')
    {
        
    var r;
    if (manual_type == undefined)
    {
        //Check whether user inserted data as DMS or DECIMAL
        r = value.match(dmsPattern);        
    }
    else
    {
        if (manual_type == 'dms')
        {
            r = value.match(dmsPattern);
        }
        else
        {
            r = null;
        }
    }    
    
    if (r) //DMS input
    {
      var hasSign = (r[1] != '');
      var hasMinutes = (r[4] != undefined);
      var hasSeconds = (r[7] != undefined);
      var MinuteHasDecimals = (r[6] != undefined);
      var direction = '';
      if (gps_type == 'latitude')
      {
        if ((r[3] == 'W' || r[3] == 'w' || r[3] == 'E' || r[3] == 'e')
            || (r[11] == 'W' || r[11] == 'w' || r[11] == 'E' || r[11] == 'e') )
        {
          showError(obj,lbl_obj,_("Latitude does not accept W/E directions, only N/S."));
          return false;
        }
        if (r[3] == 'N' || r[3] == 'n' || r[3] == 'S' || r[3] == 's')
        {
          direction = r[3];
        }
      }
      else if (gps_type == 'longitude')
      {
        if ((r[3] == 'N' || r[3] == 'n' || r[3] == 'S' || r[3] == 's')
            || (r[11] == 'N' || r[11] == 'n' || r[11] == 'S' || r[11] == 's') )
        {
          showError(obj,lbl_obj,_("Longitude does not accept N/S directions, only W/E."));
          return false;
        }
        if (r[3] == 'W' || r[3] == 'w' || r[3] == 'E' || r[3] == 'e')
        {
          direction = r[3];
        }
      }
      if ( (hasSign && ((direction != '') || (r[11] != undefined)))
            || ((direction != '') && (r[11] != undefined)) )
      {
        showError(obj,lbl_obj,_("Direction appears twice."));
        return false;
      }
      if (MinuteHasDecimals && hasSeconds)
      {
        showError(obj,lbl_obj,_("Minute decimals and seconds cannot coexist."));
        return false;
      }
      if ((r[2]*1) > 180)
      {
        showError(obj,lbl_obj,_("Degrees cannot be higher than 180."));
        return false;
      }
      if (hasMinutes && ((r[5]*1) > 59))
      {
        showError(obj,lbl_obj,_("Minutes cannot be higher than 59."));
        return false;
      }
      if (hasSeconds && ((r[8]*1) > 59))
      {
        showError(obj,lbl_obj,_("Seconds cannot be higher than 59."));
        return false;
      }
      if (!hasSign && (direction == '') && (r[11] == undefined))
      {
        if (gps_type == 'latitude') allowed_dir = 'N/S';
        else allowed_dir = 'W/E';
        showError(obj,lbl_obj,_("No direction defined. Allowed directions = ") + allowed_dir);
        return false;
      }
      //Passed all tests, now format it to standard:
      if (direction != '') gps_direction = direction.toUpperCase();
      else if (r[11] != undefined) gps_direction = r[11].toUpperCase();
      else
      {
        if (r[1] == '+')
        {
          if (gps_type == 'longitude') gps_direction = 'E';
          else gps_direction = 'N';
        }
        else
        {
          if (gps_type == 'longitude') gps_direction = 'W';
          else gps_direction = 'S';
        }
      }
      gps_degrees = r[2];
      if (hasMinutes)
      {
        gps_minutes = r[5];
        if (MinuteHasDecimals) gps_seconds = r[6] * 60;
        else
        {
          if (hasSeconds)
          {
             if (r[9] != undefined) gps_seconds = r[8] + r[9];
             else gps_seconds = r[8];
          }
          else gps_seconds = 0;
        }
      }
      else
      {
        gps_minutes = 0;
        gps_seconds = 0;
      }
      //Final adjustments
      if(isList)
      {
        obj.value = obj.value + ';' + gps_degrees + gps_direction + gps_minutes + "'" + gps_seconds + '"';
      }
      else
      {
        obj.value = gps_degrees + gps_direction + gps_minutes + "'" + gps_seconds + '"';
      }
      resetField(obj,lbl_obj);
  		return true;
    }
    else
    {
      r = value.match(decPattern);
      
      if (r) //DECIMAL input
      {
        if ((r[2]*1) > 180)
        {
          showError(obj,lbl_obj,_("Degrees cannot be higher than 180."));
          return false;
        }
        else if ((r[2]*1) == 180)
        {
          if (r[3] != '') //hasDecimals
          {
            if ((r[4]*1) > 0)
            {
              showError(obj,lbl_obj,_("Degrees cannot be higher than 180."));
              return false;
            }
          }
        }
      }
      else //Invalid format!
      {
        showError(obj,lbl_obj,_("Invalid format."));
        return false;
      }
      //Final adjustments
      if(isList)
      {
        obj.value = obj.value + ';' + value.replace(/,/g,'.');
      }
      else
      {
      obj.value = value.replace(/,/g,'.');
      }      
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