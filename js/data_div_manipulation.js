
function show(div)
{if(div=='undefined')div='general';var prefix='tab_';var divs;if(document.getElementById('tab_deposit'))
{divs=new Array('general','coll_event','isolation','identification','deposit','culture','characs','properties','quality','stock','security');}
else if(document.getElementById('tab_groups'))
{divs=new Array('general','groups','colls','subcolls','combos','dbs','configxml','divisions','templates');}
else if(document.getElementById('tab_security'))
{divs=new Array('general','security');}
else if(document.getElementById('tab_account'))
{divs=new Array('general','account');}
else
{divs=new Array('general');}
for(var x=0;x<divs.length;x++)
{$('#'+divs[x]).css('display','none');$('#'+prefix+divs[x]).attr('class','');}
$('#'+div).css('display','block');$('#'+prefix+div).attr('class','on_menu');if(document.getElementById('tab_groups'))
{change_submenu(div);}
strURL=window.location.href;if(strURL.indexOf('#')==-1)
{strURL+='#'+div+'';window.location.href=strURL;}
else
{strURL=strURL.substring(0,strURL.indexOf('#'));strURL+='#'+div+'';window.location.href=strURL;}
if($('#'+div)[0])
{$('#'+div)[0].focus();$('#'+div)[0].blur();}
showOnlyDefaultFieldTabs_Fix();}
function show_anchored_tab()
{if(location.href.indexOf("&print=1")==-1)
{div_tab=getActiveTab();show(div_tab);if(div_tab=='quality')showQuality();if(div_tab=='stock')showStock();}
else
{head=document.getElementsByTagName("head")[0];css=document.createElement('link');css.rel='stylesheet';css.href='../css/print.css';css.media='all';css.type='text/css';head.appendChild(css);window.print();}}
function showOnlyDefaultFieldTabs_Fix(){langs=document.getElementById('data_langs');if(langs==null)return;langs=langs.value.split(',');for(field in default_multi_language_fields){for(lang in langs){field_current=document.getElementById(default_multi_language_fields[field]+"_field_"+langs[lang]);if(field_current==undefined||field_current==null)continue;field_current.style.display='block';field_current.style.display='none';field_current.style.display='block';if(lang==0){field_current.style.display='block';}else{field_current.style.display='none';}}}}
addEvent(window,'load',show_anchored_tab);