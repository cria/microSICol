
function Feedback(x){}
function js_test()
{return navigator.javaEnabled();}
function detach_current(id_item_menu)
{document.getElementById(id_item_menu).style.color="#FF0000";}
function oc(a)
{var o={};for(var i=0;i<a.length;i++)
{o[a[i]]='';}
return o;}
function MaximizeMinimize(obj,prefix)
{objID=obj.parentNode.parentNode.id;objID=objID.substr(objID.lastIndexOf('_')+1);innerobj=document.getElementById(prefix+objID);if(innerobj)
{if(innerobj.style.display=='none')
{innerobj.style.display='block';obj.childNodes[0].title=_("Minimize");obj.childNodes[0].src='../img/minimize.gif';}
else
{innerobj.style.display='none';obj.childNodes[0].title=_("Maximize");obj.childNodes[0].src='../img/maximize.gif';}}
return false;}
function trim(sInString)
{sInString=sInString.replace(/^\s+/g,"");return sInString.replace(/\s+$/g,"");}
function printMe()
{strURL=location.href;index=strURL.indexOf("#");if(index!=-1)
{strURL=strURL.substring(0,index);w=window.open(strURL+'&print=1','','');}
else
{w=window.open(strURL,'','');addEvent(w,"load",print());}}
function addEvent(obj,evType,fn)
{if(obj.addEventListener)
{obj.addEventListener(evType,fn,false);return true;}
else if(obj.attachEvent)
{var r=obj.attachEvent('on'+evType,fn);return r;}
else
{return obj['on'+eType]=fn;}}
function getActiveTab()
{var _tab=window.location.href;if(_tab.indexOf('#')==_tab.length-1)
{_tab=_tab.substring(0,_tab.length-1);}
if(_tab.indexOf('#')!=-1)
{if(_tab.lastIndexOf('#')!=_tab.length-1)_tab+='#';_tab=_tab.substring(_tab.indexOf('#'));_tab=_tab.substring(1,_tab.length-1);return _tab;}
else return'general';}
function setActiveTab(_current_link)
{if(_current_link.indexOf('#')!=-1)
{_current_link=_current_link.substring(0,_current_link.indexOf('#'));}
return _current_link+'#'+getActiveTab()+'';}
function Anterior(url)
{url=url+'#'+getActiveTab()+'';window.location.href=url;}
function Proximo(url)
{url=url+'#'+getActiveTab()+'';window.location.href=url;}
function disableLink(link)
{link.style.color='#CCCCC0';link.href='#';}
function disableMenu(menu,linkpage)
{if(menu.getElementsByTagName('p'))
{var paragraphs=menu.getElementsByTagName('p');var links;for(var i=0;i<paragraphs.length;i++)
{links=paragraphs[i].getElementsByTagName('a');for(var j=0;j<links.length;j++)
{if(links[j].id!=linkpage.id)
{disableLink(links[j]);}
else
{linkpage.href='#';}}}}
else if(menu.getElementsByTagName('a'))
{for(var i=0;i<links.length;i++)
{if(links[i].id!=linkpage.id)
{disableLink(links[i]);}
else
{linkpage.href='#';}}}
else
{return false;}}
function disablePropagation(e){if(!e)e=window.event;if(e){e.cancelBubble=true;if(e.stopPropagation)e.stopPropagation();}}
function criticalPopup(e,parentId,popupId,header,criticalText,parentElementId){var image=document.getElementById(parentId);var div=document.getElementById(popupId);var currentPopup=document.getElementById("currentPopup");disablePropagation(e);if(currentPopup){if(currentPopup.value!=''){closePopup(null,currentPopup.value);}
currentPopup.value=popupId;}
div.innerHTML="<div class='critical_popup_inner' onclick='closePopup(event, \""+popupId+"\")'>"+"<div class='critical_popup_header'>"+"<table width=\"100%\" border=\"0\" cellspacing=\"1\">"+"<tr>"+"<td style='text-transform:lowercase;'>"+header+"</td>"+"<td align='right'>"+"<a style='margin-right:3px;' href='javascript:closePopup(null, \""+popupId+"\")'>X</a>"+"</td>"+"<tr>"+"</table>"+"</div>"+"<table width=\"100%\" border=\"0\" cellspacing=\"1\">"+"<tr><td>"+
criticalText+"</td><tr></table>"+"</div>";var iLeft=image.offsetLeft+image.offsetParent.offsetLeft;var iTop=image.offsetTop+image.offsetParent.offsetTop;var left=iLeft+(image.width/2);var top=iTop+(image.height/2);div.style.left=left+'px';div.style.top=top+'px';div.style.display='block';if(parentElementId){var el=document.getElementById(parentElementId);if(el.offsetHeight){var hiddenControl=document.getElementById("save_"+popupId);if(hiddenControl){hiddenControl.value=parentElementId+"|"+el.style.height;}
var minHeight=(div.offsetTop+div.offsetHeight+5);if(el.offsetHeight<minHeight){el.style.height=minHeight+'px';}}}
return false;}
function closePopup(e,popupId){var currentPopup=document.getElementById("currentPopup");var div=document.getElementById(popupId);if(currentPopup){currentPopup.value='';}
disablePropagation(e);div.style.display='none';var hiddenControl=document.getElementById("save_"+popupId);if(hiddenControl){var value=hiddenControl.value.split("|");var el=document.getElementById(value[0]);if(el.offsetHeight){el.style.height=value[1];}}}
function confirmExit()
{if(confirm(_("You are about to leave SICol. Do you confirm?"))){location.href='./subcollections.py?logout=1';return false;}}