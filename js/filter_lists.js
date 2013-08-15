
function filter_focus()
{if(document.getElementById('filter')!=null)
document.getElementById('filter').focus();}
function filter_submit()
{var txtfilter=document.getElementById('filter');if(txtfilter.value=='')
{txtfilter.value=' ';}
document.getElementById('form_filter').submit();}
addEvent(window,'load',filter_focus);