/******************************************************* 
Modified by Renato Arnellas Coelho <renatoac |at| gmail |dot| com
------------------
Added features:
- Removed some cross-browser problems
- User typed characters emphasizes eligible list
- Eligible list can have a maximum limit size (with scrollbar and key interactions)
- Eligible list is set up to be of the same size as its related input box (default size)
- All items must occupy only one row in list. If they occupy more than that then
div width is increased accordingly
------------------
AutoSuggest - a javascript automatic text input completion component
Copyright (C) 2005 Joe Kepley, The Sling & Rock Design Group, Inc.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*******************************************************
Please send any useful modifications or improvements via 
email to joekepley at yahoo (dot) com
*******************************************************/

/********************************************************
 The AutoSuggest class binds to a text input field
 and creates an automatic suggestion dropdown in the style
 of the "IntelliSense" and "AutoComplete" features of some
 desktop apps. 
 Parameters: 
 elem: A DOM element for an INPUT TYPE="text" form field
 suggestions: an array of strings to be used as suggestions
              when someone's typing.

 Example usage: 
 
 Please enter the name of a fruit.
 <input type="text" id="fruit" name="fruit" />
 <script type="text/javascript">
 var fruits=new Array("apple","orange","grape","kiwi","cumquat","banana");
 new AutoSuggest(document.getElementById("fruit"),fruits);
 </script>

 Requirements: 
 Unfortunately the AutoSuggest class doesn't seem to work 
 well with dynamically-created DIVs. So, somewhere in your 
 HTML, you'll need to add this: 
 <div id="autosuggest"><ul></ul></div>

 Here's a default set of style rules that you'll also want to 
 add to your CSS: 

 .suggestion_list
 {
 background: white;
 border: 1px solid;
 padding: 4px;
 }

 .suggestion_list ul
 {
 padding: 0;
 margin: 0;
 list-style-type: none;
 }

 .suggestion_list a
 {
 text-decoration: none;
 color: navy;
 }

 .suggestion_list .selected
 {
 background: navy;
 color: white;
 }

 .suggestion_list .selected a
 {
 color: white;
 }

 #autosuggest
 {
 display: none;
 }
*********************************************************/
//Global counter to help create unique ID's
var __idCounter = 0;

function AutoSuggest(elem, suggestions)
{
	//The 'me' variable allow you to access the AutoSuggest object
	//from the elem's event handlers defined below.
	var me = this;
	
	//Number of visible suggestions at once
	this.numRows = 0;

	//Maximum number of visible suggestions at once
	this.maxNumRows = 10;

	//Row size constant
	this.rowSize = 14;
	
	//mouse X coordinate
	this.x = 0;

	//Scrolling auxiliar values
	this.upperRow = 0;
	this.bottomRow = (this.maxNumRows - 1);
	
	//A reference to the element we're binding the list to.
	this.elem = elem;

	//Suggestions' list
	this.suggestions = suggestions;

	//Array to store a subset of eligible suggestions that match the user's input
	this.eligible = new Array();

	//The text input by the user.
	this.inputText = null;

	//A pointer to the index of the highlighted eligible item. -1 means nothing highlighted.
	this.highlighted = -1;

	//A div to use to create the dropdown.
	this.div = document.getElementById("autosuggest");
	
	//Do you want to remember what keycode means what? Me neither.
	var TAB = 9;
	var ESC = 27;
	var KEYUP = 38;
	var KEYDN = 40;
	var ENTER = 13;

	//The browsers' own autocomplete feature can be problematic, since it will 
	//be making suggestions from the users' past input.
	//Setting this attribute should turn it off.
	elem.setAttribute("autocomplete","off");

	//We need to be able to reference the elem by id. If it doesn't have an id, set one.
	if(!elem.id)
	{
		var id = "autosuggest" + __idCounter;
		__idCounter++;

		elem.id = id;
	}

	/********************************************************
	onkeydown event handler for the input elem.
	Enter key = use the highlighted suggestion, if there is one.
	Esc key = get rid of the autosuggest dropdown
	Up/down arrows = Move the highlight up and down in the suggestions.
	********************************************************/
	elem.onkeydown = function(ev)
	{
	    if (!ev) ev = window.event;
		var key = me.getKeyCode(ev);

		switch(key)
		{
			case ENTER:
			me.useSuggestion();
			break;

			case TAB:
			case ESC:
			me.hideDiv();
			break;

			case KEYUP:
			if (me.highlighted == -2)
			{
			  me.highlighted = me.eligible.length;
      }
			if (me.highlighted >= 0)
			{
				me.highlighted--;
				if (me.highlighted < me.upperRow) 
				{
					me.upperRow--;
					me.bottomRow--;
					me.div.childNodes[0].scrollTop = me.rowSize * me.upperRow;
				}
			}
			else 
			{
				me.div.childNodes[0].scrollTop = 0;
				me.upperRow = 0;
				me.bottomRow = (me.maxNumRows - 1);
			}
			me.changeHighlight(key);
			//Don't move the cursor
			return false;
			break;
			
			case KEYDN:
      if (me.highlighted < (me.eligible.length - 1))
			{
				me.highlighted++;
				if (me.highlighted > me.bottomRow) 
				{
					me.upperRow++;
					me.bottomRow++;
					me.div.childNodes[0].scrollTop = me.rowSize * me.upperRow;
				}
			}
			else me.highlighted = (me.eligible.length - 1);
			me.changeHighlight(key);
			//Don't move the cursor
			return false;
			break;
		}
		return true;
	};
	
	/********************************************************
	onkeyup handler for the elem
	If the text is of sufficient length, and has been changed, 
	then display a list of eligible suggestions.
	********************************************************/
	elem.onkeyup = function(ev) 
	{
    if (!ev) ev = window.event;
		var key = me.getKeyCode(ev);
		switch(key)
		{
			//The control keys were already handled by onkeydown, so do nothing.
			case TAB:
			case ENTER:
			case ESC:
			case KEYUP:
			case KEYDN:
				return;
			default:
				me.inputText = this.value;
				me.getEligible();
				me.createDiv();
				me.positionDiv();
				if (me.eligible.toString() != '') me.showDiv();
				else me.hideDiv();
				break;
		}
	};

	/********************************************************
	onfocus handler for the elem
	When elem get focus, show the user this elem is of autocomplete type
	********************************************************/
	elem.onfocus = function(ev)
	{
		me.inputText = this.value;
		me.getEligible();
		me.createDiv();
		me.positionDiv();
		if (me.eligible.toString() != '') me.showDiv();
		else me.hideDiv();
	};

	/********************************************************
	onblur handler for the elem
	If the elem loses focus, then remove autocomplete div.
	********************************************************/
	this.onBlurEvent = function(ev)
	{
		//No focus, no autocomplete
		me.hideDiv();
		/* In case it loses focus to a mouse click event, make sure it is an onmousedown event because it is called
		first in the hierarchy than this onblur event, otherwise the user would click on an invisible DIV... */
	};
	
	elem.onblur = me.onBlurEvent;
	
	/********************************************************
	Insert the highlighted suggestion into the input box, and 
	remove the suggestion dropdown.
	********************************************************/
	this.useSuggestion = function()
	{
		if (this.highlighted > -1)
		{
			this.elem.value = this.eligible[this.highlighted];
			if (elem.onchange) elem.onchange();
			this.hideDiv();
		}
	};

	/********************************************************
	Display the dropdown. Pretty straightforward.
	********************************************************/
	this.showDiv = function()
	{
		this.div.style.display = 'block';
	};

	/********************************************************
	Hide the dropdown and clear any highlight.
	********************************************************/
	this.hideDiv = function()
	{
		this.div.style.display = 'none';
		this.highlighted = -1;
	};

	/********************************************************
	Modify the HTML in the dropdown to move the highlight.
	********************************************************/
	this.changeHighlight = function()
	{
		var lis = this.div.getElementsByTagName('LI');
		for (i in lis)
		{
			var li = lis[i];
			if (this.highlighted == i)
			{
				if (typeof(li) == "object") li.className = "selected";
			}
			else
			{
				if (typeof(li) == "object") li.className = "";
			}
		}
	};
	
	/********************************************************
	Position the dropdown div below the input text field.
	********************************************************/
	this.positionDiv = function()
	{
		var el = this.elem;
		var x = 0;
		var y = el.offsetHeight * 2; //initial offset (show autocomplete below input)
		//Walk up the DOM and add up all of the offset positions.
		while (el.offsetParent)
		{
			x += el.offsetLeft;
			y += el.offsetTop;
			el = el.offsetParent;
		}
		/*
		For some reason there is an extra offset due to "div #general .data" element
		Therefore use this widget only on formularies
			  ^
			  |
			  133
			  |
			  v
		<----> GENERAL
		*/
		if (navigator.userAgent.indexOf("MSIE") != -1) // IE
		{
			x += el.offsetLeft - 38;
		}
		else //FF
		{
			x += el.offsetLeft - 18;
		}
		
		y += el.offsetTop - 133;
		this.div.style.left = x + 'px';
		this.div.style.top = y + 'px';
	};

	/********************************************************
	Build the HTML for the dropdown div
	********************************************************/
	this.createDiv = function()
	{
		var ul = document.createElement('ul');
		ul.style.width = ((this.elem.clientWidth*1) - (this.elem.offsetLeft*1) - 14) + 'px';
		ul.style.overflow = 'scroll';
		//Create an array of LI's for the words.
		for (i=0;i<this.eligible.length; i++)
		{
                    var word = this.eligible[i];
    
                    var li = document.createElement('li');
                    var a = document.createElement('a');
                    a.href="javascript:false";
                    //Emphasize input text
                    foundword = '<b>'+word.substr(0,this.inputText.length)+'</b>';
                    restword = word.substr(this.inputText.length);
                    a.innerHTML = foundword + restword;
                    
                    li.appendChild(a);
                    if (me.highlighted == i)
                    {
                            li.className = "selected";
                    }
                    ul.appendChild(li);
		}
		//Increase width while there are items which use more than one row
		addwidth = 0;
		add_amount = 10;
		//Create a blacklist of items that use more than one row
		blacklist = new Array();
		this.div.replaceChild(ul,this.div.childNodes[0]);
		this.showDiv();
		lis = ul.getElementsByTagName('LI');
		for(i in lis)
		{
			if (!isNaN(parseInt(i)))
			{
				liheight = lis[i].offsetHeight / 14;
				if (liheight > 1)
        {
          blacklist.push(lis[i]);
        } 
			}
		}
		while (blacklist.length > 0)
		{
  		addwidth += add_amount;
   		ul.style.width = (addwidth+(this.elem.clientWidth - this.elem.offsetLeft - 2)) + 'px';
  		this.div.replaceChild(ul,this.div.childNodes[0]);
  		clonelist = blacklist.concat(); //clone the array
  		blacklist = new Array();
		  for(i in clonelist)
		  {
				liheight = clonelist[i].offsetHeight / 14;
				if (liheight > 1)
				{
           blacklist.push(clonelist[i]);
        }
      }
      if (blacklist.length == 0)
      {
    		addwidth += add_amount;
      }
    }
 		if (this.inputText.length > 0) addwidth += 10; //extra space for bold characters
 		ul.style.width = (addwidth+(this.elem.clientWidth - this.elem.offsetLeft - 2)) + 'px';
		ul.style.height = (this.rowSize*this.numRows ) + 'px';
		this.div.replaceChild(ul,this.div.childNodes[0]);

		/********************************************************
		mouseover handler for the dropdown ul
		move the highlighted suggestion with the mouse
		********************************************************/
		ul.onmouseover = function(ev)
		{
			//Walk up from target until you find the LI.
			var target = me.getEventSource(ev);
			while (target.parentNode && target.tagName.toUpperCase() != 'LI')
			{
				target = target.parentNode;
			}
		
			var lis = me.div.getElementsByTagName('LI');
			
			for (i in lis)
			{
				var li = lis[i];
				if(li == target)
				{
					me.highlighted = i;
					break;
				}
			}

			me.changeHighlight();

			//Recalculate upper and bottom limits according to mouseover selection
			if (me.highlighted > (me.maxNumRows-1)) //index starts from zero
			{
			    me.upperRow = Math.round(me.div.childNodes[0].scrollTop / me.rowSize);
				me.bottomRow = me.upperRow + (me.maxNumRows - 1);
			}
			else
			{
				me.upperRow = 0;
				me.bottomRow = me.maxNumRows - 1;
			}
		};

		/********************************************************
		click handler for the dropdown ul
		insert the clicked suggestion into the input
		********************************************************/
		ul.onmousedown = function(ev)
		{
			listwidth = ul.style.width;
			listwidth = listwidth.substring(0,listwidth.length-2) * 1;
			listoffset = me.div.style.left;
			listoffset = listoffset.substring(0,listoffset.length-2) * 1;
			//Check whether we are clicking on the scrollbar or on a list item
			if (me.x > (listwidth + listoffset - 50) && me.x < (listwidth + listoffset + 50))//48(odd offset) - 10(width of scrollbar)
			{
				if (document.all)
				{
					//IE scrollbar fix
					me.elem.ondblclick = me.elem.onblur;
					me.elem.onblur = null;
					me.div.onblur = me.elem.ondblclick;
					setTimeout("document.getElementById('"+me.elem.id+"').onblur = document.getElementById('"+me.elem.id+"').ondblclick;document.getElementById('"+me.elem.id+"').ondblclick = null;",100);
				}
				//Scrollbar was hit, pass this event to scrollbar handler
				return true;
			}
			me.useSuggestion();
			me.hideDiv();
			me.cancelEvent(ev);
			return false;
		};
		
		ul.onmousemove = function(ev)
		{
			if (!ev) ev = window.event;
			if (ev.clientX) //IE
			{
				me.x = ev.clientX;
			}
			else //FF
			{
				me.x = ev.pageX;
			}
		};
		
		this.div.className="suggestion_list";
		this.div.style.position = 'absolute';
		this.div.setAttribute('nowrap','nowrap');
	};

  this.ignoreAccentedCharacters = function(word)
  {
      //Attention: in order to make this work, this file must be saved in UTF-8 format!
      word = word.replace(/[áàãäâ]/,"a");
      word = word.replace(/[éèêë]/,"e");
      word = word.replace(/[íìîï]/,"i");
      word = word.replace(/[óòõôö]/,"o");
      word = word.replace(/[úùûü]/,"u");
      return word;
  };

	/********************************************************
	determine which of the suggestions matches the input
	********************************************************/
	this.getEligible = function()
	{
		this.numRows = 0;
		this.eligible = new Array();
		for (i=0;i<this.suggestions.length;i++) 
		{
                        var suggestion = this.suggestions[i];
                        if(this.ignoreAccentedCharacters(suggestion.toLowerCase()).indexOf(this.ignoreAccentedCharacters(this.inputText.toLowerCase())) == "0")
                        {
                            this.eligible[this.eligible.length]=suggestion;
                            this.numRows++;
                        }
		}
		if (this.numRows > this.maxNumRows)
                    this.numRows = this.maxNumRows;
	};

	/********************************************************
	Helper function to determine the keycode pressed in a 
	browser-independent manner.
	********************************************************/
	this.getKeyCode = function(ev)
	{
		if(ev) //Moz
		{
			return ev.keyCode;
		}
		if(window.event) //IE
		{
			return window.event.keyCode;
		}
	};

	/********************************************************
	Helper function to determine the event source element in a 
	browser-independent manner.
	********************************************************/
	this.getEventSource = function(ev)
	{
		if(ev) //Moz
		{
			return ev.target;
		}
		if(window.event) //IE
		{
			return window.event.srcElement;
		}
	};

	/********************************************************
	Helper function to cancel an event in a 
	browser-independent manner.
	(Returning false helps too).
	********************************************************/
	this.cancelEvent = function(ev)
	{
		if(ev) //Moz
		{
			ev.preventDefault();
			ev.stopPropagation();
		}
		if(window.event) //IE
		{
			window.event.returnValue = false;
		}
	};
}
