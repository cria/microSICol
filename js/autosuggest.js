
var __idCounter=0;function AutoSuggest(elem,suggestions)
{var me=this;this.numRows=0;this.maxNumRows=10;this.rowSize=14;this.x=0;this.upperRow=0;this.bottomRow=(this.maxNumRows-1);this.elem=elem;this.suggestions=suggestions;this.eligible=new Array();this.inputText=null;this.highlighted=-1;this.div=document.getElementById("autosuggest");var TAB=9;var ESC=27;var KEYUP=38;var KEYDN=40;var ENTER=13;elem.setAttribute("autocomplete","off");if(!elem.id)
{var id="autosuggest"+__idCounter;__idCounter++;elem.id=id;}
elem.onkeydown=function(ev)
{if(!ev)ev=window.event;var key=me.getKeyCode(ev);switch(key)
{case ENTER:me.useSuggestion();break;case TAB:case ESC:me.hideDiv();break;case KEYUP:if(me.highlighted==-2)
{me.highlighted=me.eligible.length;}
if(me.highlighted>=0)
{me.highlighted--;if(me.highlighted<me.upperRow)
{me.upperRow--;me.bottomRow--;me.div.childNodes[0].scrollTop=me.rowSize*me.upperRow;}}
else
{me.div.childNodes[0].scrollTop=0;me.upperRow=0;me.bottomRow=(me.maxNumRows-1);}
me.changeHighlight(key);return false;break;case KEYDN:if(me.highlighted<(me.eligible.length-1))
{me.highlighted++;if(me.highlighted>me.bottomRow)
{me.upperRow++;me.bottomRow++;me.div.childNodes[0].scrollTop=me.rowSize*me.upperRow;}}
else me.highlighted=(me.eligible.length-1);me.changeHighlight(key);return false;break;}
return true;};elem.onkeyup=function(ev)
{if(!ev)ev=window.event;var key=me.getKeyCode(ev);switch(key)
{case TAB:case ENTER:case ESC:case KEYUP:case KEYDN:return;default:me.inputText=this.value;me.getEligible();me.createDiv();me.positionDiv();if(me.eligible.toString()!='')me.showDiv();else me.hideDiv();break;}};elem.onfocus=function(ev)
{me.inputText=this.value;me.getEligible();me.createDiv();me.positionDiv();if(me.eligible.toString()!='')me.showDiv();else me.hideDiv();};this.onBlurEvent=function(ev)
{me.hideDiv();};elem.onblur=me.onBlurEvent;this.useSuggestion=function()
{if(this.highlighted>-1)
{this.elem.value=this.eligible[this.highlighted];if(elem.onchange)elem.onchange();this.hideDiv();}};this.showDiv=function()
{this.div.style.display='block';};this.hideDiv=function()
{this.div.style.display='none';this.highlighted=-1;};this.changeHighlight=function()
{var lis=this.div.getElementsByTagName('LI');for(i in lis)
{var li=lis[i];if(this.highlighted==i)
{if(typeof(li)=="object")li.className="selected";}
else
{if(typeof(li)=="object")li.className="";}}};this.positionDiv=function()
{var el=this.elem;var x=0;var y=el.offsetHeight*2;while(el.offsetParent)
{x+=el.offsetLeft;y+=el.offsetTop;el=el.offsetParent;}
if(navigator.userAgent.indexOf("MSIE")!=-1)
{x+=el.offsetLeft-38;}
else
{x+=el.offsetLeft-18;}
y+=el.offsetTop-133;this.div.style.left=x+'px';this.div.style.top=y+'px';};this.createDiv=function()
{var ul=document.createElement('ul');ul.style.width=((this.elem.clientWidth*1)-(this.elem.offsetLeft*1)-14)+'px';ul.style.overflow='scroll';for(i=0;i<this.eligible.length;i++)
{var word=this.eligible[i];var li=document.createElement('li');var a=document.createElement('a');a.href="javascript:false";foundword='<b>'+word.substr(0,this.inputText.length)+'</b>';restword=word.substr(this.inputText.length);a.innerHTML=foundword+restword;li.appendChild(a);if(me.highlighted==i)
{li.className="selected";}
ul.appendChild(li);}
addwidth=0;add_amount=10;blacklist=new Array();this.div.replaceChild(ul,this.div.childNodes[0]);this.showDiv();lis=ul.getElementsByTagName('LI');for(i in lis)
{if(!isNaN(parseInt(i)))
{liheight=lis[i].offsetHeight/14;if(liheight>1)
{blacklist.push(lis[i]);}}}
while(blacklist.length>0)
{addwidth+=add_amount;ul.style.width=(addwidth+(this.elem.clientWidth-this.elem.offsetLeft-2))+'px';this.div.replaceChild(ul,this.div.childNodes[0]);clonelist=blacklist.concat();blacklist=new Array();for(i in clonelist)
{liheight=clonelist[i].offsetHeight/14;if(liheight>1)
{blacklist.push(clonelist[i]);}}
if(blacklist.length==0)
{addwidth+=add_amount;}}
if(this.inputText.length>0)addwidth+=10;ul.style.width=(addwidth+(this.elem.clientWidth-this.elem.offsetLeft-2))+'px';ul.style.height=(this.rowSize*this.numRows)+'px';this.div.replaceChild(ul,this.div.childNodes[0]);ul.onmouseover=function(ev)
{var target=me.getEventSource(ev);while(target.parentNode&&target.tagName.toUpperCase()!='LI')
{target=target.parentNode;}
var lis=me.div.getElementsByTagName('LI');for(i in lis)
{var li=lis[i];if(li==target)
{me.highlighted=i;break;}}
me.changeHighlight();if(me.highlighted>(me.maxNumRows-1))
{me.upperRow=Math.round(me.div.childNodes[0].scrollTop/me.rowSize);me.bottomRow=me.upperRow+(me.maxNumRows-1);}
else
{me.upperRow=0;me.bottomRow=me.maxNumRows-1;}};ul.onmousedown=function(ev)
{listwidth=ul.style.width;listwidth=listwidth.substring(0,listwidth.length-2)*1;listoffset=me.div.style.left;listoffset=listoffset.substring(0,listoffset.length-2)*1;if(me.x>(listwidth+listoffset-50)&&me.x<(listwidth+listoffset+50))
{if(document.all)
{me.elem.ondblclick=me.elem.onblur;me.elem.onblur=null;me.div.onblur=me.elem.ondblclick;setTimeout("document.getElementById('"+me.elem.id+"').onblur = document.getElementById('"+me.elem.id+"').ondblclick;document.getElementById('"+me.elem.id+"').ondblclick = null;",100);}
return true;}
me.useSuggestion();me.hideDiv();me.cancelEvent(ev);return false;};ul.onmousemove=function(ev)
{if(!ev)ev=window.event;if(ev.clientX)
{me.x=ev.clientX;}
else
{me.x=ev.pageX;}};this.div.className="suggestion_list";this.div.style.position='absolute';this.div.setAttribute('nowrap','nowrap');};this.ignoreAccentedCharacters=function(word)
{word=word.replace(/[áàãäâ]/,"a");word=word.replace(/[éèêë]/,"e");word=word.replace(/[íìîï]/,"i");word=word.replace(/[óòõôö]/,"o");word=word.replace(/[úùûü]/,"u");return word;};this.getEligible=function()
{this.numRows=0;this.eligible=new Array();for(i=0;i<this.suggestions.length;i++)
{var suggestion=this.suggestions[i];if(this.ignoreAccentedCharacters(suggestion.toLowerCase()).indexOf(this.ignoreAccentedCharacters(this.inputText.toLowerCase()))=="0")
{this.eligible[this.eligible.length]=suggestion;this.numRows++;}}
if(this.numRows>this.maxNumRows)
this.numRows=this.maxNumRows;};this.getKeyCode=function(ev)
{if(ev)
{return ev.keyCode;}
if(window.event)
{return window.event.keyCode;}};this.getEventSource=function(ev)
{if(ev)
{return ev.target;}
if(window.event)
{return window.event.srcElement;}};this.cancelEvent=function(ev)
{if(ev)
{ev.preventDefault();ev.stopPropagation();}
if(window.event)
{window.event.returnValue=false;}};}