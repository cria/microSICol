// JavaScript Document 

//Function to filter list
/*function filter_lists(object, table_id)
{
	var mytable = document.getElementById(table_id);
	var tbody = mytable.getElementsByTagName("tbody")[0];
	var rows = tbody.getElementsByTagName("tr");
	var enter_text = object.value.toLowerCase(); //get enter text as case-insensitive

	for (var i = rows.length; i--;) //search all rows on table
	{
		var tr = rows[i]; //get row node
		var cols = tr.getElementsByTagName("td"); //get columns list from row
		for(var j = cols.length; j--;) //search all columns on row
		{
			var col = cols[j]; //get column node
			if (!col.firstChild) continue; //jump if not value
			var text = col.firstChild.nodeValue.toLowerCase(); //get node value as case-insensitive
			//Attention! IE ignores extra spaces when getting nodeValue. Example: String "ABC  DE" has nodeValue "ABC DE". 
			//This may cause problems when comparing strings using the indexOf function.
			var tr_display = false; //start as False
			if (enter_text != '')
			{
				if((enter_text.indexOf('(') != -1) || (enter_text.indexOf(')') != -1)) //if typed parenthesis
				{
					if (text.indexOf(enter_text) != -1) //if match
					{
						tr_display = true;
						break;
					}
				}
				else //if not typed parenthesis
				{
					text = text.replace(/\(|\)/g,''); //replace parenthesis
					if(text.indexOf(enter_text) != -1) //if match
					{
						tr_display = true;
						break;
					}
				}
			}
			else //if text typed
			{
				tr_display = true;
				break;
			}
		}
		if (tr_display) tr.style.display = '' //return to default style
		else tr.style.display = 'none'; //hide <tr></tr>
	}
}*/

function filter_focus()
{
	if (document.getElementById('filter') != null)
		document.getElementById('filter').focus();
}


function filter_submit()
{  
  var txtfilter = document.getElementById('filter');
  
  //Persist data of filter in the server
  if (txtfilter.value == '')
  {
  	txtfilter.value = ' ';
  }
   
  document.getElementById('form_filter').submit();
}

//Add event for window.onload
addEvent(window, 'load', filter_focus);
