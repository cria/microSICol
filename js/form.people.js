
var multi_language_fields=new Array();multi_language_fields.push("comments");var default_multi_language_fields=new Array();default_multi_language_fields.concat(multi_language_fields);default_multi_language_fields.push("comments");var mapTextArea=new Object();mapTextArea['address']=65535;mapTextArea['phone']=65535;mapTextArea['comments_*']=65535;function validatePeople()
{errors=false;form=document.getElementById('edit');people_name=document.getElementsByName('name')[0];lbl_name=getLabel('name');email=document.getElementsByName('email')[0];lbl_email=getLabel('email');resetField(email,lbl_email);resetField(people_name,lbl_name);if(!checkOneEmail(email,lbl_email,true))errors=true;if(!isValidTextArea('address',65535))errors=true;if(!isValidTextArea('phone',65535))errors=true;langs=document.getElementById('data_langs').value;langs=langs.split(',');for(mlf in multi_language_fields)
{max_size=mapTextArea[multi_language_fields[mlf]+'_*'];for(lang in langs)
{if(!isValidTextArea(multi_language_fields[mlf]+'_'+langs[lang],max_size))errors=true;}}
if(isEmpty(people_name,lbl_name))errors=true;return errors;}
function disableLinks()
{disableMenu(document.getElementById('menu'),document.getElementById('active_people'));disableLink(document.getElementById('active_preferences'));disableLink(document.getElementById('active_configuration'));disableLink(document.getElementById('active_utilities'));}
addEvent(window,'load',disableLinks);