// JavaScript Document 

function insert_contact(counter, inserted_after)
{
  if (inserted_after && document.getElementById("ins_select_inst").selectedIndex == 0)
  {
	 alert (_("Please, enter a valid Institution."));
	 return;
  }
  
  if (inserted_after && !checkEmailNoLabel(document.getElementById("ins_text_email"),true))	return;
  var i = 0;
  _table = document.getElementById("people_contacts");
  _all_rows = _table.getElementsByTagName ("tr");
  /* 1 to get as the first line of the table, after the headers, at row 0 */
  _our_row = _all_rows[1];
  _new_row = document.createElement("tr");

  _td1 = document.createElement("td");
  _td1.Class = "people_contacts_first";

  //Institution Field 
  _span_inst = document.createElement("span");
  _span_inst.id = "span_inst_"  + counter;
  _span_inst.style.display = "none";
  /* Another javascript trap: the onclick value must be a javascript function, not  a  string! */
  _span_inst.onclick = new Function ("edit_contact(" + counter + ");");
  _span_inst.title = _("click to edit");
  //Must be style.cursor
  _span_inst.style.cursor = "pointer";
  _td1.appendChild (_span_inst);
  //Create the select institution form element for this contact
  _select_institution = build_select_inst(counter);
  _td1.appendChild (_select_institution);
  //Insert column in the table
  _new_row.appendChild (_td1);
  
  //Contact Field
  _td2 = document.createElement("td");
  _span_contact = '\n<span id="span_contact_' + counter + '" class="click_edit" style="display: none;" title="'+_("click to edit")+'" onclick="javascript:edit_contact(' + counter + ')"></span>';
  _check_contact = '\n<input type="checkbox" id="check_contact_' + counter + '" name="check_contact_' + counter + '" class="checkbox" value="YES">';
  _td2.innerHTML =  _span_contact + _check_contact;
  _new_row.appendChild(_td2);

  /* KISS: next TDs are created with innerHTML. TD1 needed DOM due <select> form element */
  //Department Field
  _td3 = document.createElement("td");
  _span_dep = '\n<span id="span_dep_' + counter + '" class="click_edit" style="display: none;" title="'+_("click to edit")+'" onclick="javascript:edit_contact(' + counter + ')"></span>';
  _text_dep =  '\n<input type="text" id="text_dep_' + counter + '" name="text_dep_' + counter + '" class="text" style="display: inline" maxlength="80" value="" />';
  _td3.innerHTML = _span_dep + _text_dep;
  _new_row.appendChild(_td3);
  
  //E-Mail Field
  _td4 = document.createElement("td");
  _span_email = '\n<span id="span_email_' + counter + '" class="click_edit" style="display: none;" title="'+_("click to edit")+'" onclick="javascript:edit_contact(' + counter + ')"></span>';
  _text_email = '\n<input type="text" id="text_email_' + counter + '" name="text_email_' + counter + '" class="text" style="display: inline" maxlength="100" value="" />';
  _td4.innerHTML = _span_email + _text_email;
  _new_row.appendChild(_td4);
  
  //Buttons (set, edit and delete)
  _td5 = document.createElement("td");
  _td5.setAttribute("nowrap","nowrap");
  _td5.style.width = "50px";
  
  /*_link_edit = '\n<input type="button" id="link_edit_' + counter + '" class="button" style="display: none" onclick="javascript:edit_contact(' + counter + ')" value="'+_("Edit")+'" />';
  _link_set = '\n<input type="button" id="link_set_' + counter + '" class="button" style="display: inline" onclick="javascript:set_contact(' + counter + ')" value="'+_("Set")+'" />';
  _link_delete = '\n<input type="button" id="link_delete_' + counter + '" class="button" style="display: inline" onclick="javascript:delete_contact(' + counter + ')" value="'+_("Delete")+'" />\n';*/
  
  _link_edit = '\n<img src="../img/edit.png" id="link_edit_' + counter + '" style="display: inline; cursor: pointer;" onclick="javascript:edit_contact(' + counter + ')" title="'+_("Edit")+'" />';
  _link_set = '\n<img src="../img/apply.png" id="link_set_' + counter + '" style="display: inline; cursor: pointer;" onclick="javascript:set_contact(' + counter + ')" title="'+_("Set")+'" />';
  _link_delete = '\n<img src="../img/delete.png" id="link_delete_' + counter + '" style="display: inline; cursor: pointer;" onclick="javascript:delete_contact(' + counter + ')" title="'+_("Delete")+'" />\n';

  _td5.innerHTML = _link_edit + _link_set + _link_delete;
  _new_row.appendChild(_td5);

  _table.tBodies[0].appendChild(_new_row);
  _last_ct_index++;
  
  if (inserted_after)
	{
		insert_after(counter);
	}

  return counter;
}

function insert_after(counter)
{
   var widget_institution_ins = document.getElementById("ins_select_inst");
   var widget_contact_ins = document.getElementById("ins_check_contact");
   var widget_department_ins = document.getElementById("ins_text_dep");
   var widget_email_ins = document.getElementById("ins_text_email");
   
   var widget_institution = document.getElementById("select_inst_" + counter);
   var widget_contact = document.getElementById("check_contact_" + counter);
   var widget_department = document.getElementById("text_dep_" + counter);
   var widget_email= document.getElementById("text_email_" + counter);
   
   set_selected (widget_institution, widget_institution_ins.options[widget_institution_ins.selectedIndex].value);
   widget_contact.checked = widget_contact_ins.checked;
   widget_department.value = widget_department_ins.value;
   widget_email.value = widget_email_ins.value;
   set_contact(counter);
   
   widget_institution_ins.selectedIndex = 0;
   widget_contact_ins.checked = false;
   widget_department_ins.value = "";
   widget_email_ins.value = "";
}

function set_contact (ct_index)
{
  span_institution = document.getElementById("span_inst_" + ct_index);
  select_institution = document.getElementById("select_inst_" + ct_index);
  span_contact = document.getElementById("span_contact_" + ct_index);
  check_contact = document.getElementById("check_contact_" + ct_index);
  span_dep = document.getElementById("span_dep_" + ct_index);
  text_dep = document.getElementById("text_dep_" + ct_index);
  span_email = document.getElementById("span_email_" + ct_index);
  text_email = document.getElementById("text_email_" + ct_index);
  link_edit = document.getElementById("link_edit_" + ct_index);
  link_set = document.getElementById("link_set_" + ct_index);
  link_delete = document.getElementById("link_delete_" + ct_index);
    
  if (select_institution.selectedIndex == 0)
	{
		alert (_("Please, enter a valid Institution."));
		return;
	}
	if (!checkEmailNoLabel(text_email,true)) return;

  _inst_name = "";
  for (i = 0; i < _inst_ids.length; i++)
  {
     if (_inst_ids[i] == select_institution.value)
     {
        _inst_name = _inst_names[i];
        if (_inst_nicks[i]) _inst_name = _inst_name + "(" + _inst_nicks[i] + ")";
        break;
     }
  }
  span_institution.innerHTML= _inst_name;
  span_contact.innerHTML = (check_contact.checked?' ['+_("contact")+']': "");
  span_dep.innerHTML=text_dep.value;
	span_email.innerHTML=text_email.value;

  select_institution.style.display="none";
  check_contact.style.display="none";
  text_dep.style.display="none";
  text_email.style.display="none";
  link_set.style.display="none";
  link_delete.style.display="none";

  span_institution.style.display="inline";
  span_contact.style.display="inline";
  span_dep.style.display="inline";
  span_email.style.display="inline";
  link_edit.style.display="inline";
}

function edit_contact (ct_index)
{
  span_institution = document.getElementById("span_inst_" + ct_index);
  select_institution = document.getElementById("select_inst_" + ct_index);
  span_contact = document.getElementById("span_contact_" + ct_index);
  check_contact = document.getElementById("check_contact_" + ct_index);
  span_dep = document.getElementById("span_dep_" + ct_index);
  text_dep = document.getElementById("text_dep_" + ct_index);
  span_email = document.getElementById("span_email_" + ct_index);
  text_email = document.getElementById("text_email_" + ct_index);
  link_edit = document.getElementById("link_edit_" + ct_index);
  link_set = document.getElementById("link_set_" + ct_index);
  link_delete = document.getElementById("link_delete_" + ct_index);

  span_institution.style.display="none";
  span_contact.style.display="none";
  span_dep.style.display="none";
  span_email.style.display="none";
  link_edit.style.display="none";

  select_institution.style.display="inline";
  check_contact.style.display="inline";
  text_dep.style.display="inline";
  text_email.style.display="inline";
  link_set.style.display="inline";
  link_delete.style.display="inline";
}

function delete_contact(counter)
{
  /* simply deletes the whole table row that contains the data to be erased.
   if data on a contact is not transmited back to the cgi script, it is
   deleted */
  element = document.getElementById("select_inst_" + counter);
  tries = 0;
  while (element.nodeName != "TR" && tries < 20)
  {
      element = element.parentNode;
      tries ++;
  }
  if (tries < 20)
  {
      parent_ = element.parentNode;
      parent_.removeChild(element);
      element.innerHTML = "";
  }
}

/*
Builds "Select Institution" form element with data from inst_ids and inst_names arrays
*/
function build_select_inst(counter)
{
    var i = 0;
    /* Uses global arrays inst_ids, inst_names setup by the cgi script in the html body */
    _select_inst = document.createElement("select");
    _select_inst.id = "select_inst_" + counter;
    _select_inst.name = "select_inst_" + counter;
    _select_inst.style.display = "inline";
    _select_inst.onchange = "update_inst_sel()";
	
    opt = document.createElement("option");
    opt.value = "-1";
    opt.innerHTML = "---";
    opt.selected = true;
    _select_inst.appendChild(opt);
    for (i = 0; i < _inst_ids.length; i++)
    {
        opt = document.createElement("option");
        opt.value = _inst_ids[i];
        opt.innerHTML= _inst_names[i] + "\n";
        _select_inst.appendChild(opt);
    }
    return _select_inst;
}
  
function build_contact_list()
{
   /* Uses global arrays cont_*  dynamically appended  part */
   var i = 0;
   for (i = 0; i < _cont_inst_ids.length; i++)
   {
	   insert_contact(i, false);
	   
	   _inst_id_widget = document.getElementById("select_inst_" + i);
	   
	   set_selected (_inst_id_widget, _cont_inst_ids[i]);
	   _inst_id_span = document.getElementById("span_inst_" + i);
	   _inst_id_span.innerHTML = make_inst_name (i);
	   _check_contact = document.getElementById("check_contact_" + i);
	   if (_cont_contact[i]) _check_contact.checked = true;
	   _text_dep = document.getElementById("text_dep_" + i);
	   _text_dep.value = _cont_department[i];
	   _span_dep = document.getElementById("span_dep_" + i);
	   _span_dep.innerHTML = _cont_department[i];
	   _text_email = document.getElementById("text_email_" + i);
	   _text_email.value = _cont_email[i];
	   _span_email = document.getElementById("span_email_" + i);
	   _span_email.innerHTML = _cont_email[i];
	   set_contact (i);
  }
  _last_ct_index = i;
}
 
function set_selected(widget, value)
{
  options = widget.getElementsByTagName("option");
	for (i = 0; i < options.length; i++)
  {
	    if (options[i].value == value) options[i].selected = true;
  	 	else options[i].selected = false;
  }
}

function make_inst_name (i)
{
  str = _inst_names[i];
	if (_inst_nicks[i]) str += " (" + _inst_nicks[i] + ") ";
	if (_cont_contact[i]) str += ' [' + _("contact") + ']';
}

function delete_unused_contacts ()
{ /*Uses global variable last_ct_index*/
  for (i = 0; i < _last_ct_index; i++)
  {
      _inst_sel_array = document.getElementsByName("select_inst_" + i);
      if (! _inst_sel_array.length) continue;
      _inst_sel = _inst_sel_array[0];
      if (_inst_sel.value == "-1")
      {
          delete_contact(i);
      }
  }
}

function in_array (element, array)
{
  var i;
  for (i in array)
  {
     if (array[i] == element) return true;
  }
  return false;
}
  
function validateContact()
{
  /*Uses global variables last_ct_index, inst_ids, inst_values*/
  var i, j;
  var errors = false;
  delete_unused_contacts();
  used = new Array();
  counter = 0;
  for (i = 0; i < _last_ct_index; i++)
  {
     _inst_sel_array = document.getElementsByName("select_inst_" + i);
     if (! _inst_sel_array.length) continue;
     _inst_sel = _inst_sel_array[0];
     if (_inst_sel.style.display != "none")
     {
       errors = true;
  	   alert(_("There are institutions in edit mode. Please, check before continuing."));
  	   break;
     }
     for(j = counter; j--  && used[j] !== _inst_sel.value;);
     if (j != -1)
     {
       errors = true;
  	   alert(_("There are duplicated institutions in contacts"));
  	   break;
     }
     used [counter++] = _inst_sel.value;
  }
  return errors;
}
