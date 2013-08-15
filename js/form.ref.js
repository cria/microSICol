
var multi_language_fields=new Array();multi_language_fields.push("comments");var default_multi_language_fields=new Array();default_multi_language_fields.concat(multi_language_fields);default_multi_language_fields.push("comments");var mapTextArea=new Object();mapTextArea['url']=65535;mapTextArea['comments_*']=65535;function validateReference()
{errors=false;title=document.getElementsByName('title')[0];lbl_title=getLabel('title');url=document.getElementsByName('url')[0];lbl_url=getLabel('url');resetField(url,lbl_url);if(!isValidTextArea('url',65535))errors=true;langs=document.getElementById('data_langs').value;langs=langs.split(',');for(mlf in multi_language_fields)
{max_size=mapTextArea[multi_language_fields[mlf]+'_*'];for(lang in langs)
{if(!isValidTextArea(multi_language_fields[mlf]+'_'+langs[lang],max_size))errors=true;}}
title.value=tinyMCE.get('title').getContent();if(isEmpty(title,lbl_title))errors=true;return errors;}
function checkYear(obj,lbl_obj,minYear,maxYear)
{if(lbl_obj==null)lbl_obj=getLabel(obj.id);if(obj.value!='')
{if(!ValidYear(obj.value))
{showError(obj,lbl_obj,_("Invalid year."));return false;}
else if(maxYear!=-1)
{if(obj.value>maxYear||obj.value<minYear)
{showError(obj,lbl_obj,_("Invalid year."));return false;}
else
{resetField(obj,lbl_obj);return true;}}
else
{resetField(obj,lbl_obj);return true;}}
else
{resetField(obj,lbl_obj);return true;}}
function disableLinks()
{disableMenu(document.getElementById('menu'),document.getElementById('active_references'));disableLink(document.getElementById('active_preferences'));disableLink(document.getElementById('active_configuration'));disableLink(document.getElementById('active_utilities'));}
addEvent(window,'load',disableLinks);