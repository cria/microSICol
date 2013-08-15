
function init(){switch_fields('system');prepare_select();document.getElementById('copyleft_bar').style.textAlign='left';document.getElementById('copyleft_bar').style.paddingLeft='10px';}
function switch_fields(tl_type)
{switch(tl_type)
{case"system":document.getElementById('system_fields').style.display='';document.getElementById('report_fields').style.display='none';break;case"report":document.getElementById('system_fields').style.display='none';document.getElementById('report_fields').style.display='';break;}}
function sortlist(fields){var lb=document.getElementById(fields);var arrTexts=new Array();var hash={};for(i=0;i<lb.length;i++){arrTexts[i]=lb.options[i].text;hash[lb.options[i].text]=lb.options[i].value;}
arrTexts.sort();for(i=0;i<lb.length;i++){lb.options[i].text=arrTexts[i];lb.options[i].value=hash[arrTexts[i]];}}
function prepare_select(){var id=location.search.split('&')[0].split('=')[1];if(id=='header_template'||id=='footer_template'){document.getElementById('sel_field').remove(1);}
else{if(id=='data_template'){}
else{var field=location.search.split('&')[2].split('=')[1];var label=decodeURIComponent(location.search).split('&')[1].split('=')[1];document.getElementById('sel_report_fields').options.length=0;document.getElementById('sel_report_fields').options[document.getElementById('sel_report_fields').options.length]=new Option(label,field);}
document.getElementById('sel_field').selectedIndex=1;switch_fields('report');}
sortlist('sel_report_fields');sortlist('sel_system_fields');}
function insertAtCursor(myField,myValue){if(window.opener.document.selection){myField.focus();sel=window.opener.document.selection.createRange();sel.text=myValue;}
else if(myField.selectionStart||myField.selectionStart=='0'){var startPos=myField.selectionStart;var endPos=myField.selectionEnd;myField.value=myField.value.substring(0,startPos)+myValue+myField.value.substring(endPos,myField.value.length);}
else{myField.value+=myValue;}}
function Insert()
{var sel_field=document.getElementById('sel_field');var tl=null;switch(sel_field.options[sel_field.selectedIndex].value){case'system':var sel_system=document.getElementById('sel_system_fields');tl='[FIELD:'+sel_system.options[sel_system.selectedIndex].value+']';break;case'report':var sel_report=document.getElementById('sel_report_fields');tl='[FIELD:'+sel_report.options[sel_report.selectedIndex].value+']';break;}
var id=decodeURIComponent(location.search).split('&')[0].split('=')[1];insertAtCursor(window.opener.document.getElementById(id),tl);window.close();}