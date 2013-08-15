
function do_check(obj)
{var this_user_id=document.getElementById('util_user_id').value;if(this_user_id==1&&obj.id=='userrole_2')
{alert(_("Unable to remove Administrator function."));return false;}
else if(obj.id=='userrole_2')
{disable_status=false;if(obj.checked)disable_status=true;for(i in useralldel_areas)
{if(i==1)
{chk_id=useralldel_areas[i];if(document.getElementById(chk_id).checked)
{document.getElementById(chk_id).checked=false;}
else
{document.getElementById(chk_id).checked=true;}
document.getElementById(chk_id).disabled=true;}
else
{chk_id=useralldel_areas[i];document.getElementById(chk_id).checked=true;document.getElementById(chk_id).disabled=disable_status;}}
for(i in userallcreate_areas)
{chk_id=userallcreate_areas[i];document.getElementById(chk_id).checked=true;document.getElementById(chk_id).disabled=disable_status;}
for(i in all_colls)
{chk_id=all_colls[i];document.getElementById(chk_id).checked=true;document.getElementById(chk_id).disabled=disable_status;}
return true;}}
function delete_user(id)
{if(id==_current_id_user)
{alert(_("It is not possible to delete yourself."));}
else if(id==1)
{alert(_("It is not possible to delete super user."));}
else if(confirm(_("Delete User. Are you sure?")))
{document.getElementById('util_type').value='user_delete';document.getElementById('util_form').submit();}}
function new_user()
{clear_submenu();add_submenu_button("save_user();",_("Save User"),"save");add_submenu_button("cancel_user();",_("Cancel"),"cancel");document.getElementById('util_user_id').value='';document.getElementById('util_user_login').value='';document.getElementById('pwd_msg').innerHTML='';document.getElementById('util_user_name').value='';document.getElementById('util_user_comments').value='';for(i in useralldel_areas)
{if(i==1)
{chk_id=useralldel_areas[i];document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=true;}
else
{chk_id=useralldel_areas[i];document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=false;}}
for(i in userallcreate_areas)
{chk_id=userallcreate_areas[i];document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=false;}
for(i in all_colls)
{chk_id=all_colls[i];document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=false;}
for(i in all_roles)
{chk_id=all_roles[i];document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=false;}
document.getElementById('util_edit_user').style.display='block';}
function save_user()
{_user_id=document.getElementById('util_user_id').value;_user_login=document.getElementById('util_user_login').value;_user_name=document.getElementById('util_user_name').value;_user_pwd=document.getElementById('util_user_pwd').value;_user_pwd_confirm=document.getElementById('util_user_pwd_confirm').value;if(_user_name==''||_user_login=='')
{alert(_("Please fill in the Login and Name fields."));return;}
if(!(_user_id)&&_user_pwd=='')
{alert(_("Please fill in the Password field."));return;}
if(_user_pwd!=_user_pwd_confirm)
{alert(_("Passwords do not match."));return;}
document.getElementById('util_type').value='user';document.getElementById('util_form').submit();return;}
function edit_user(_id,_login,_name,_comments,_access,_groups,_areas)
{new_user();add_submenu_button("delete_user("+_id+");",_("Delete"),"delete");document.getElementById('util_user_id').value=_id;document.getElementById('util_user_login').value=_login;document.getElementById('pwd_msg').innerHTML=_("Leave blank to maintain previous password.");document.getElementById('util_user_name').value=_name;document.getElementById('util_user_comments').value=_comments;is_admin=false;if(_groups!='')
{_groups_list=_groups.split(",");for(i in _groups_list)
{chk_id=_groups_list[i];if(chk_id=='userrole_2')is_admin=true;document.getElementById(chk_id).checked=true;}}
if(_access!='')
{_access_list=_access.split(",");for(i in _access_list)
{chk_id=_access_list[i];document.getElementById(chk_id).checked=true;}}
for(i in all_colls)
{chk_id=all_colls[i];if(is_admin)document.getElementById(chk_id).disabled=true;else document.getElementById(chk_id).disabled=false;}
if(is_admin)
{for(i in useralldel_areas)
{chk_id=useralldel_areas[i];document.getElementById(chk_id).checked=true;document.getElementById(chk_id).disabled=true;}
for(i in userallcreate_areas)
{chk_id=userallcreate_areas[i];document.getElementById(chk_id).checked=true;document.getElementById(chk_id).disabled=true;}}
else
{for(i in useralldel_areas)
{chk_id=useralldel_areas[i];if(i==1)
{document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=true;}
else
{document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=false;}}
for(i in userallcreate_areas)
{chk_id=userallcreate_areas[i];document.getElementById(chk_id).checked='';document.getElementById(chk_id).disabled=false;}
if(_areas!='')
{_areas_list=_areas.split(",");for(i in _areas_list)
{chk_id=_areas_list[i];document.getElementById(chk_id).checked=true;}}}}
function cancel_user()
{clear_submenu();add_submenu_button("new_user();",_("Create New User"),"new");}
function delete_group(id)
{if(id==2)
{alert(_("Unable to delete Administrator Level."));}
else
{if(confirm(_("Delete Group. Are you sure?")))
{document.getElementById('util_type').value='role_delete';document.getElementById('util_form').submit();}}}
function new_group()
{clear_submenu();add_submenu_button("save_group();",_("Save Group"),"save");add_submenu_button("cancel_group();",_("Cancel"),"cancel");document.getElementById('util_role_id').value='';document.getElementById('util_role_name').value='';document.getElementById('util_role_descr').value='';document.getElementById('util_role_type').selectedIndex=0;document.getElementById('util_group_members').options.length=0;document.getElementById('util_group_possible_members').innerHTML='';for(i in alldel_areas)
{chk_id=alldel_areas[i];if(i==1)
{document.getElementById(chk_id).disabled=true;}
document.getElementById(chk_id).checked='';}
for(i in allcreate_areas)
{chk_id=allcreate_areas[i];document.getElementById(chk_id).checked=true;}
document.getElementById('util_group_possible_members').innerHTML='';for(var i=0;i<_grouparray_possible_members.length;i++)
{var oLang=document.createElement("option");oLang.value=_grouparray_possible_members[i][1];oLang.text=_grouparray_possible_members[i][0];oLang.innerText=_grouparray_possible_members[i][0];document.getElementById('util_group_possible_members').appendChild(oLang);}
document.getElementById('util_edit_role').style.display='block';}
function edit_group(_id,_name,_descr,_type,_areas,_members)
{new_group();add_submenu_button("delete_group("+_id+");",_("Delete"),"delete");document.getElementById('util_role_id').value=_id;if(_type=='user')
{document.getElementById('opt_role_type_group').style.display='none';document.getElementById('opt_role_type_level').style.display='none';document.getElementById('opt_role_type_user').style.display='block';document.getElementById('p_role_name').style.display='none';sel=document.getElementById('util_role_type').selectedIndex=2;}
else
{document.getElementById('opt_role_type_group').style.display='block';document.getElementById('opt_role_type_level').style.display='block';document.getElementById('opt_role_type_user').style.display='none';document.getElementById('p_role_name').style.display='block';sel=document.getElementById('util_role_type');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_type)sel.selectedIndex=i;}}
document.getElementById('util_role_name').value=_name;document.getElementById('util_role_descr').value=_descr;for(i in alldel_areas)
{chk_id=alldel_areas[i];if(i==1)
{document.getElementById(chk_id).disabled=true;}
document.getElementById(chk_id).checked='';}
for(i in allcreate_areas)
{chk_id=allcreate_areas[i];document.getElementById(chk_id).checked='';}
if(_areas!='')
{_areas_list=_areas.split(",");for(i in _areas_list)
{chk_id=_areas_list[i];document.getElementById(chk_id).checked=true;}}
var array_members=_members.split(";");if(array_members[0]!='')
{for(var i=0;i<array_members.length;i++)
{var oLang=document.createElement("option");currmember=array_members[i].split(",");oLang.value=currmember[1];oLang.text=currmember[0];oLang.innerText=currmember[0];document.getElementById('util_group_members').appendChild(oLang);}}
document.getElementById('util_group_possible_members').innerHTML='';for(var i=0;i<_grouparray_possible_members.length;i++)
{var already_has=false;for(var j=0;j<array_members.length;j++)
{this_member=array_members[j].split(",");possible_member=_grouparray_possible_members[i];if(this_member[1]==possible_member[1])
{already_has=true;}}
if(!already_has)
{var oLang=document.createElement("option");currmember=_grouparray_possible_members[i];oLang.value=currmember[1];oLang.text=currmember[0];oLang.innerText=currmember[0];document.getElementById('util_group_possible_members').appendChild(oLang);}}}
function save_group()
{_group_name=document.getElementById('util_role_name').value;if(_group_name=='')
{alert(_("Please fill in the Name field."));}
else
{var obj=document.getElementById('util_group_members');for(i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
document.getElementById('util_type').value='role';document.getElementById('util_form').submit();}}
function cancel_group()
{clear_submenu();add_submenu_button("new_group();",_("Create New Group"),"new");}
function delete_coll(id)
{if(id==_current_id_coll)
{alert(_("Unable to delete current Collection."));}
else if(confirm(_("Delete Collection. Are you sure?")))
{document.getElementById('util_type').value='coll_delete';document.getElementById('util_form').submit();}}
function new_coll()
{clear_submenu();add_submenu_button("save_coll();",_("Save Collection"),"save");add_submenu_button("cancel_coll();",_("Cancel"),"cancel");document.getElementById('util_coll_id').value='';document.getElementById('util_coll_base').selectedIndex=0;document.getElementById('util_coll_code').value='';document.getElementById('util_coll_name').value='';document.getElementById('util_logo_msg').innerHTML="<br /><br /><img src=\"logo.py\" width=\"130\" height=\"30\" />";document.getElementById('util_edit_coll').style.display='block';}
function edit_coll(_id,_base,_code,_descr,_has_logo)
{new_coll();add_submenu_button("delete_coll("+_id+");",_("Delete"),"delete");document.getElementById('util_coll_id').value=_id;sel=document.getElementById('util_coll_base');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_base)sel.selectedIndex=i;}
document.getElementById('util_coll_code').value=_code;document.getElementById('util_coll_name').value=_descr;if(_has_logo=='1')document.getElementById('util_logo_msg').innerHTML="<br /><br /><img src='logo.py?id="+_id+"' width=\"130\" height=\"30\" />";else document.getElementById('util_logo_msg').innerHTML="<br /><br /><img src='logo.py' width=\"130\" height=\"30\" />";}
function save_coll()
{_coll_id=document.getElementById('util_coll_id').value;_coll_code=document.getElementById('util_coll_code').value;if(_coll_code=='')
{alert(_("Please fill in the Code field."));}
else
{document.getElementById('util_type').value='coll';document.getElementById('util_form').submit();}}
function cancel_coll()
{clear_submenu();add_submenu_button("new_coll();",_("Create New Collection"),"new");}
function delete_subcoll(id)
{if(id==_current_id_subcoll)
{alert(_("Unable to delete current Subcollection."));}
else if(confirm(_("Delete Subcollection. Are you sure?")))
{document.getElementById('util_type').value='subcoll_delete';document.getElementById('util_form').submit();}}
function new_subcoll()
{clear_submenu();add_submenu_button("save_subcoll();",_("Save Subcollection"),"save");add_submenu_button("cancel_subcoll();",_("Cancel"),"cancel");document.getElementById('util_subcoll_id').value='';document.getElementById('util_subcoll_coll').selectedIndex=0;document.getElementById('util_subcoll_code').value='';document.getElementById('util_subcoll_name').value='';document.getElementById('util_subcoll_dateinput').selectedIndex=0;document.getElementById('util_subcoll_dateoutput').selectedIndex=0;document.getElementById('util_subcoll_data_lang').options.length=0;document.getElementById('util_subcoll_possible_data_lang').innerHTML='';document.getElementById('util_subcoll_lang').selectedIndex=0;for(var i=0;i<_array_possible_data_langs.length;i++)
{var oLang=document.createElement("option");oLang.value=_array_possible_data_langs[i];oLang.text=_array_possible_data_langs[i];oLang.innerText=_array_possible_data_langs[i];document.getElementById('util_subcoll_possible_data_lang').appendChild(oLang);}
document.getElementById('util_edit_subcoll').style.display='block';}
function edit_subcoll_template(select){clear_submenu();tinyMCE.get('header_template').execCommand('mceSetContent',false,'');tinyMCE.get('footer_template').execCommand('mceSetContent',false,'');tinyMCE.get('css_template').execCommand('mceSetContent',false,'');var val=Number(select.value);if(val!=0){add_submenu_button("save_subcoll_template("+val+");",_("Save Template"),"save");tinyMCE.get('header_template').execCommand('mceSetContent',false,select.options[select.selectedIndex].attributes.header.value);tinyMCE.get('footer_template').execCommand('mceSetContent',false,select.options[select.selectedIndex].attributes.footer.value);tinyMCE.get('css_template').execCommand('mceSetContent',false,select.options[select.selectedIndex].attributes.styles.value);}
else{}}
function save_subcoll_template(){document.getElementById('util_type').value='template';document.getElementById('util_form').submit();}
function edit_subcoll(_id,_coll,_name,_descr,_input,_output,_lang,_data_lang)
{new_subcoll();add_submenu_button("delete_subcoll("+_id+");",_("Delete"),"delete");document.getElementById('util_subcoll_id').value=_id;sel=document.getElementById('util_subcoll_coll');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_coll)sel.selectedIndex=i;}
document.getElementById('util_subcoll_code').value=_name;document.getElementById('util_subcoll_name').value=_descr;sel=document.getElementById('util_subcoll_dateinput');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_input)sel.selectedIndex=i;}
sel=document.getElementById('util_subcoll_dateoutput');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_output)sel.selectedIndex=i;}
var array_data_langs=_data_lang.split(",");if(array_data_langs[0]!='')
{for(var i=0;i<array_data_langs.length;i++)
{var oLang=document.createElement("option");oLang.value=array_data_langs[i];oLang.text=array_data_langs[i];oLang.innerText=array_data_langs[i];document.getElementById('util_subcoll_data_lang').appendChild(oLang);}}
document.getElementById('util_subcoll_possible_data_lang').innerHTML='';for(var i=0;i<_array_possible_data_langs.length;i++)
{var already_has=false;for(var j=0;j<array_data_langs.length;j++)
{if(_array_possible_data_langs[i]==array_data_langs[j])
{already_has=true;}}
if(!already_has)
{var oLang=document.createElement("option");oLang.value=_array_possible_data_langs[i];oLang.text=_array_possible_data_langs[i];oLang.innerText=_array_possible_data_langs[i];document.getElementById('util_subcoll_possible_data_lang').appendChild(oLang);}}
sel=document.getElementById('util_subcoll_lang');if(_lang=='')_lang='default';for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_lang)sel.selectedIndex=i;}}
function save_subcoll()
{_subcoll_id=document.getElementById('util_subcoll_id').value;_subcoll_code=document.getElementById('util_subcoll_code').value;if(_subcoll_code=='')
{alert(_("Please fill in the Name field."));document.getElementById('util_subcoll_code').focus();return;}
if(document.getElementById('util_subcoll_data_lang').options.length==0)
{alert(_("Please, choose one or more input languages."));document.getElementById('util_subcoll_possible_data_lang').focus();return;}
var obj=document.getElementById('util_subcoll_data_lang');for(i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
document.getElementById('util_type').value='subcoll';document.getElementById('util_form').submit();}
function cancel_subcoll()
{clear_submenu();add_submenu_button("new_subcoll();",_("Create New Subcollection"),"new");}
function init_combo(_id,_coll_subcoll,_taxon_groups,_str_types,_dep_reasons,_preservation_methods,_test_groups,foredit,ignoreButtons)
{var edit_combo_prefix="edit_combo("+"'"+_id+"',"+"'"+_coll_subcoll+"',"+"'"+_taxon_groups+"',"+"'"+_str_types+"',"+"'"+_dep_reasons+"',"+"'"+_preservation_methods+"',"+"'"+_test_groups+"',";if(!ignoreButtons){clear_submenu();if(foredit){add_submenu_button("save_combo();",_("Save Subcollection Combo Configuration"),"save");add_submenu_button(edit_combo_prefix+"false);",_("Cancel"),"cancel");}
else{foredit=false;clear_submenu();add_submenu_button(edit_combo_prefix+"true);",_("Edit Subcollection Combo Configuration"),"edit");}}
document.getElementById('util_combo_id').value='';document.getElementById('util_combo_taxon_group').options.length=0;document.getElementById('util_combo_possible_taxon_group').innerHTML='';document.getElementById('util_combo_str_type').options.length=0;document.getElementById('util_combo_possible_str_type').innerHTML='';document.getElementById('util_combo_dep_reason').options.length=0;document.getElementById('util_combo_possible_dep_reason').innerHTML='';document.getElementById('util_combo_preservation_method').options.length=0;document.getElementById('util_combo_possible_preservation_method').innerHTML='';document.getElementById('util_combo_test_group').options.length=0;document.getElementById('util_combo_possible_test_group').innerHTML='';for(var i=0;i<_array_possible_taxon_groups.length;i++)
{var opt=document.createElement("option");opt.value=_array_possible_taxon_groups[i][1];opt.text=_array_possible_taxon_groups[i][0];var has_hierarchy=parseInt(_array_possible_taxon_groups[i][2]);opt.setAttribute("title",opt.text);opt.innerText=_array_possible_taxon_groups[i][0];if(!has_hierarchy)
{opt.setAttribute("blame",1);}
document.getElementById('util_combo_possible_taxon_group').disabled=!foredit;}
for(var i=0;i<_array_possible_str_types.length;i++)
{var opt=document.createElement("option");opt.value=_array_possible_str_types[i][1];opt.text=_array_possible_str_types[i][0];opt.setAttribute("title",opt.text);opt.innerText=_array_possible_str_types[i][0];document.getElementById('util_combo_possible_str_type').appendChild(opt);document.getElementById('util_combo_possible_str_type').disabled=!foredit;}
for(var i=0;i<_array_possible_dep_reasons.length;i++)
{var opt=document.createElement("option");opt.value=_array_possible_dep_reasons[i][1];opt.text=_array_possible_dep_reasons[i][0];opt.setAttribute("title",opt.text);opt.innerText=_array_possible_dep_reasons[i][0];document.getElementById('util_combo_possible_dep_reason').appendChild(opt);document.getElementById('util_combo_possible_dep_reason').disabled=!foredit;}
for(var i=0;i<_array_possible_preservation_methods.length;i++)
{var opt=document.createElement("option");opt.value=_array_possible_preservation_methods[i][1];opt.text=_array_possible_preservation_methods[i][0];opt.setAttribute("title",opt.text);opt.innerText=_array_possible_preservation_methods[i][0];document.getElementById('util_combo_possible_preservation_method').appendChild(opt);document.getElementById('util_combo_possible_preservation_method').disabled=!foredit;}
for(var i=0;i<_array_possible_test_groups.length;i++)
{var opt=document.createElement("option");opt.value=_array_possible_test_groups[i][1];opt.text=_array_possible_test_groups[i][0];opt.setAttribute("title",opt.text);opt.innerText=_array_possible_test_groups[i][0];document.getElementById('util_combo_possible_test_group').appendChild(opt);document.getElementById('util_combo_possible_test_group').disabled=!foredit;}
document.getElementById('util_edit_combo').style.display='block';document.getElementById('util_combo_taxon_group').disabled=!foredit;document.getElementById('util_combo_str_type').disabled=!foredit;document.getElementById('util_combo_dep_reason').disabled=!foredit;document.getElementById('util_combo_preservation_method').disabled=!foredit;document.getElementById('util_combo_test_group').disabled=!foredit;document.getElementById('combo_str_type_en').disabled=!foredit;document.getElementById('combo_str_type_ptbr').disabled=!foredit;document.getElementById('combo_dep_reason_en').disabled=!foredit;document.getElementById('combo_dep_reason_ptbr').disabled=!foredit;document.getElementById('combo_test_group_en').disabled=!foredit;document.getElementById('combo_test_group_ptbr').disabled=!foredit;document.getElementById('combo_preservation_method_en').disabled=!foredit;document.getElementById('combo_preservation_method_ptbr').disabled=!foredit;document.getElementById('combo_unit_measure_en').disabled=!foredit;document.getElementById('combo_unit_measure_ptbr').disabled=!foredit;}
function edit_combo(_id,_coll_subcoll,_taxon_groups,_str_types,_dep_reasons,_preservation_methods,_test_groups,enabled,ignoreButtons)
{if(!enabled){enabled=false;}
init_combo(_id,_coll_subcoll,_taxon_groups,_str_types,_dep_reasons,_preservation_methods,_test_groups,enabled,ignoreButtons);document.getElementById('util_combo_id').value=_id;document.getElementById('combo_current_subcoll').innerHTML=_coll_subcoll;document.getElementById('division_current_subcoll').innerHTML=_coll_subcoll;var array_taxon_groups=_taxon_groups.split(",");var oc_taxon_groups=oc(array_taxon_groups);document.getElementById('util_combo_possible_taxon_group').innerHTML='';for(var i=0;i<_array_possible_taxon_groups.length;i++)
{var opt=document.createElement("option");currtype=_array_possible_taxon_groups[i];opt.value=currtype[1];opt.text=currtype[0];opt.setAttribute("title",opt.text);opt.innerText=currtype[0];if(currtype[1]in oc_taxon_groups)
{opt.selected=true;}
if(!enabled){opt.readOnly=true;}
var has_hierarchy=parseInt(currtype[2]);if(!has_hierarchy)
{opt.setAttribute("blame",1);}
document.getElementById('util_combo_possible_taxon_group').appendChild(opt);}
var array_str_types=_str_types.split(",");var oc_str_types=oc(array_str_types);document.getElementById('util_combo_possible_str_type').innerHTML='';for(var i=0;i<_array_possible_str_types.length;i++)
{var opt=document.createElement("option");currtype=_array_possible_str_types[i];opt.value=currtype[1];opt.text=currtype[0];opt.setAttribute("title",opt.text);opt.innerText=currtype[0];if(currtype[1]in oc_str_types)
{opt.selected=true;}
document.getElementById('util_combo_possible_str_type').appendChild(opt);}
var array_dep_reasons=_dep_reasons.split(",");var oc_dep_reasons=oc(array_dep_reasons);document.getElementById('util_combo_possible_dep_reason').innerHTML='';for(var i=0;i<_array_possible_dep_reasons.length;i++)
{var opt=document.createElement("option");currtype=_array_possible_dep_reasons[i];opt.value=currtype[1];opt.text=currtype[0];opt.setAttribute("title",opt.text);opt.innerText=currtype[0];if(currtype[1]in oc_dep_reasons)
{opt.selected=true;}
document.getElementById('util_combo_possible_dep_reason').appendChild(opt);}
var array_preservation_methods=_preservation_methods.split(",");var oc_preservation_methods=oc(array_preservation_methods);document.getElementById('util_combo_possible_preservation_method').innerHTML='';for(var i=0;i<_array_possible_preservation_methods.length;i++)
{var opt=document.createElement("option");currtype=_array_possible_preservation_methods[i];opt.value=currtype[1];opt.text=currtype[0];opt.setAttribute("title",opt.text);opt.innerText=currtype[0];if(currtype[1]in oc_preservation_methods)
{opt.selected=true;}
document.getElementById('util_combo_possible_preservation_method').appendChild(opt);}
var array_test_groups=_test_groups.split(",");var oc_test_groups=oc(array_test_groups);document.getElementById('util_combo_possible_test_group').innerHTML='';for(var i=0;i<_array_possible_test_groups.length;i++)
{var opt=document.createElement("option");currtype=_array_possible_test_groups[i];opt.value=currtype[1];opt.text=currtype[0];opt.setAttribute("title",opt.text);opt.innerText=currtype[0];if(currtype[1]in oc_test_groups)
{opt.selected=true;}
document.getElementById('util_combo_possible_test_group').appendChild(opt);}
change_item('util_combo_possible_taxon_group','util_combo_taxon_group',0);change_item('util_combo_possible_str_type','util_combo_str_type',0);change_item('util_combo_possible_dep_reason','util_combo_dep_reason',0);change_item('util_combo_possible_preservation_method','util_combo_preservation_method',0);change_item('util_combo_possible_test_group','util_combo_test_group',0);}
function validateCombo(prefix)
{var new_item=true;for(var i=0;i<_array_possible_data_langs.length;i++)
{if(i==0)
{if(document.getElementById(prefix+_array_possible_data_langs[i]).value=='')
{new_item=false;}}
else
{if(document.getElementById(prefix+_array_possible_data_langs[i]).value==''&&new_item)
{alert(_("Please, fill in all language fields if a new item is to be inserted."));return false;}
else if(document.getElementById(prefix+_array_possible_data_langs[i]).value!=''&&!new_item)
{alert(_("Please, fill in all language fields if a new item is to be inserted."));return false;}}}
return true;}
function save_combo()
{_combo_id=document.getElementById('util_combo_id').value;validateCombo('combo_str_type_');if(document.getElementById('util_combo_taxon_group').options.length==0)
{alert(_("Please, choose one or more Taxon Groups for this Subcollection."));document.getElementById('util_combo_possible_taxon_group').focus();return;}
if(document.getElementById('util_combo_str_type').options.length==0)
{alert(_("Please, choose one or more Strain Types for this Subcollection."));document.getElementById('util_combo_possible_str_type').focus();return;}
validateCombo('combo_dep_reason_');if(document.getElementById('util_combo_dep_reason').options.length==0)
{alert(_("Please, choose one or more Strain Deposit Types for this Subcollection."));document.getElementById('util_combo_possible_dep_reason').focus();return;}
validateCombo('combo_preservation_method_');if(document.getElementById('util_combo_preservation_method').options.length==0)
{alert(_("Please, choose one or more Preservation Methods for this Subcollection."));document.getElementById('util_combo_possible_preservation_method').focus();return;}
validateCombo('combo_test_group_');if(document.getElementById('util_combo_test_group').options.length==0)
{alert(_("Please, choose one or more Test Groups for this Subcollection."));document.getElementById('util_combo_possible_test_group').focus();return;}
var obj=null;obj=document.getElementById('util_combo_taxon_group');for(var i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
obj=document.getElementById('util_combo_str_type');for(var i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
obj=document.getElementById('util_combo_dep_reason');for(var i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
obj=document.getElementById('util_combo_preservation_method');for(var i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
obj=document.getElementById('util_combo_test_group');for(var i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
document.getElementById('util_type').value='combo';document.getElementById('util_combo_langs').value=_array_possible_data_langs.join(",");document.getElementById('util_form').submit();}
function cancel_combo()
{clear_submenu();}
function delete_base()
{if(confirm(_("Delete base reference. Are you sure?")))
{document.getElementById('util_type').value='dbs_delete';document.getElementById('util_form').submit();}}
function new_base()
{clear_submenu();add_submenu_button("save_base();",_("Save Base"),"save");add_submenu_button("cancel_base();",_("Cancel"),"cancel");document.getElementById('util_base_id').value='';document.getElementById('util_base_dbms').selectedIndex=0;document.getElementById('util_base_host').value='';document.getElementById('util_base_port').value='';document.getElementById('util_base_name').value='';document.getElementById('util_base_user').value='';document.getElementById('util_base_pwd').value='';document.getElementById('util_base_tracebility_dbms').selectedIndex=0;document.getElementById('util_base_tracebility_host').value='';document.getElementById('util_base_tracebility_port').value='';document.getElementById('util_base_tracebility_name').value='';document.getElementById('util_base_tracebility_user').value='';document.getElementById('util_base_tracebility_pwd').value='';document.getElementById('util_edit_base').style.display='block';}
function edit_base(_id,_dbms,_host,_port,_db_name,_user,_pwd,_tracebility_id,_tracebility_dbms,_tracebility_host,_tracebility_port,_tracebility_db_name,_tracebility_user,_tracebility_pwd)
{new_base();add_submenu_button("delete_base();",_("Delete"),"delete");document.getElementById('util_base_id').value=_id;sel=document.getElementById('util_base_dbms');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_dbms)sel.selectedIndex=i;}
document.getElementById('util_base_host').value=_host;document.getElementById('util_base_port').value=_port;document.getElementById('util_base_name').value=_db_name;document.getElementById('util_base_user').value=_user;document.getElementById('util_base_pwd').value=_pwd;document.getElementById('util_base_tracebility_id').value=_tracebility_id;sel=document.getElementById('util_base_tracebility_dbms');for(var i=0;i<sel.options.length;i++)
{if(sel.options[i].value==_tracebility_dbms)sel.selectedIndex=i;}
document.getElementById('util_base_tracebility_host').value=_tracebility_host;document.getElementById('util_base_tracebility_port').value=_tracebility_port;document.getElementById('util_base_tracebility_name').value=_tracebility_db_name;document.getElementById('util_base_tracebility_user').value=_tracebility_user;document.getElementById('util_base_tracebility_pwd').value=_tracebility_pwd;}
function save_base()
{_base_id=document.getElementById('util_base_id').value;_db_host=document.getElementById('util_base_host').value;_db_port=document.getElementById('util_base_port').value;_db_name=document.getElementById('util_base_name').value;_tracebility_db_host=document.getElementById('util_base_tracebility_host').value;_tracebility_db_port=document.getElementById('util_base_tracebility_port').value;_tracebility_db_name=document.getElementById('util_base_tracebility_name').value;if(_db_host==''||_db_port==''||_db_name==''||_tracebility_db_host==''||_tracebility_db_port==''||_tracebility_db_name=='')
{alert(_("Please fill in the following fields:")+' '+_("Data Host")+', '+_("Data Port")+', '+_("Data Name")+', '+_("Tracebility Host")+', '+_("Tracebility Port")+', '+_("Tracebility Name"));}
else
{document.getElementById('util_type').value='dbs';document.getElementById('util_form').submit();}}
function cancel_base()
{clear_submenu();add_submenu_button("new_base();",_("Create New Base"),"new");}
function delete_division()
{if(confirm(_("Delete division. Are you sure?")))
{document.getElementById('util_type').value='division_delete';document.getElementById('util_form').submit();}}
function new_division()
{clear_submenu();add_submenu_button("save_division();",_("Save Division"),"save");add_submenu_button("cancel_division();",_("Cancel"),"cancel");document.getElementById('util_division_id').value='';document.getElementById('util_division_division').value='';document.getElementById('util_division_pattern').value='';document.getElementById('util_edit_division').style.display='block';}
function edit_division(_id,_division,_pattern)
{new_division();add_submenu_button("delete_division();",_("Delete"),"delete");document.getElementById('util_division_id').value=_id;document.getElementById('util_division_division').value=_division;document.getElementById('util_division_pattern').value=_pattern;}
function save_division()
{_division_id=document.getElementById('util_division_id').value;_division_division=document.getElementById('util_division_division').value;_division_pattern=document.getElementById('util_division_pattern').value;if(_division_division==''||_division_pattern=='')
{alert(_("Please fill in the following fields:")+' '+_("Division")+', '+_("Pattern"));return;}
else if(_division_pattern.indexOf('#')==-1)
{alert(_("Please fill pattern field with at least one #."));return;}
else
{document.getElementById('util_type').value='division';document.getElementById('util_form').submit();}}
function cancel_division()
{clear_submenu();add_submenu_button("new_division();",_("Create New Division"),"new");}
function save_config()
{if(document.getElementById('util_config_data_lang').options.length==0)
{alert(_("Please, choose one or more input languages."));document.getElementById('util_config_possible_data_lang').focus();return;}
_config_inputurl=document.getElementById('util_config_indexurl').value;_config_rootdir=document.getElementById('util_config_rootdir').value;if(_config_inputurl==''||_config_rootdir=='')
{alert(_("Please fill in the following fields:")+' '+_("Index URL")+', '+_("Root Directory"));return;}
var obj=document.getElementById('util_config_data_lang');for(i=0;i<obj.options.length;i++)
{obj.options[i].selected=true;}
document.getElementById('util_type').value='configxml';alert(_("Effects will take place after re-entering the system."));document.getElementById('util_form').submit();}
function init_config_fields(indexurl,rootdir,inputmask,outputmask,_data_lang,uploadlimit)
{var i=0;document.getElementById('util_config_indexurl').value=indexurl;document.getElementById('util_config_rootdir').value=rootdir;document.getElementById('util_config_upload').value=uploadlimit;sel=document.getElementById('util_config_dateinput');for(i=0;i<sel.length;i++)
{if(sel.options[i].value==inputmask)sel.selectedIndex=i;}
sel=document.getElementById('util_config_dateoutput');for(i=0;i<sel.length;i++)
{if(sel.options[i].value==inputmask)sel.selectedIndex=i;}
document.getElementById('util_config_possible_data_lang').innerHTML='';for(var i=0;i<_configarray_possible_data_langs.length;i++)
{var oLang=document.createElement("option");oLang.value=_configarray_possible_data_langs[i];oLang.text=_configarray_possible_data_langs[i];oLang.innerText=_configarray_possible_data_langs[i];document.getElementById('util_config_possible_data_lang').appendChild(oLang);}
var array_data_langs=_data_lang.split(",");if(array_data_langs[0]!='')
{for(var i=0;i<array_data_langs.length;i++)
{var oLang=document.createElement("option");oLang.value=array_data_langs[i];oLang.text=array_data_langs[i];oLang.innerText=array_data_langs[i];document.getElementById('util_config_data_lang').appendChild(oLang);}}
document.getElementById('util_config_possible_data_lang').innerHTML='';for(var i=0;i<_array_possible_data_langs.length;i++)
{var already_has=false;for(var j=0;j<array_data_langs.length;j++)
{if(_array_possible_data_langs[i]==array_data_langs[j])
{already_has=true;}}
if(!already_has)
{var oLang=document.createElement("option");oLang.value=_array_possible_data_langs[i];oLang.text=_array_possible_data_langs[i];oLang.innerText=_array_possible_data_langs[i];document.getElementById('util_config_possible_data_lang').appendChild(oLang);}}}
function send()
{document.getElementById('util_form').submit();}
function add_submenu_button(action,_title,_content)
{if(_content=='')return;sub=document.getElementById('submenu');for(var i=0;i<sub.childNodes.length;i++)
{if(sub.childNodes[i].tagName=='P')
{sub_p=sub.childNodes[i];break;}}
img=document.createElement('img');switch(_content)
{case'new':img.src='../img/record_add.png';break;case'edit':img.src='../img/record_edit.png';break;case'save':img.src='../img/record_save.png';break;case'cancel':img.src='../img/record_cancel.png';break;case'delete':img.src='../img/record_delete.png';break;default:break;}
img.title=_title;img.onclick=function(){eval(action);};img.style.marginLeft="7px";img.style.cursor="pointer";sub_p.appendChild(img);}
function clear_submenu()
{sub=document.getElementById('submenu');for(var i=0;i<sub.childNodes.length;i++)
{if(sub.childNodes[i].tagName=='P')
{sub_p=sub.childNodes[i];break;}}
sub_p.innerHTML='';document.getElementById('util_edit_user').style.display='none';document.getElementById('util_edit_base').style.display='none';document.getElementById('util_edit_coll').style.display='none';document.getElementById('util_edit_subcoll').style.display='none';document.getElementById('util_edit_combo').style.display='none';document.getElementById('util_edit_role').style.display='none';document.getElementById('util_edit_division').style.display='none';}
function change_submenu(item)
{document.getElementById("util_form").action="./configuration.py#"+item;switch(item)
{case'general':clear_submenu();add_submenu_button("new_user();",_("Create New User"),"new");break;case'groups':clear_submenu();add_submenu_button("new_group();",_("Create New Group"),"new");break;case'colls':clear_submenu();add_submenu_button("new_coll();",_("Create New Collection"),"new");break;case'subcolls':clear_submenu();add_submenu_button("new_subcoll();",_("Create New Subcollection"),"new");break;case'combos':clear_submenu();startComboSettings(1);break;case'dbs':clear_submenu();add_submenu_button("new_base();",_("Create New Base"),"new");break;case'divisions':clear_submenu();add_submenu_button("new_division();",_("Create New Division"),"new");break;case'templates':clear_submenu();add_submenu_button("save_subcoll_template();",_("Save Template"),"save");break;case'configxml':clear_submenu();add_submenu_button("save_config();",_("Save config.xml"),"save");break;default:break;}}
function change_item(id_fieldOrig,id_fieldDest,client_action)
{var fieldOrig=document.getElementById(id_fieldOrig);var fieldDest=document.getElementById(id_fieldDest);x=fieldOrig.value;ListAvailable=fieldOrig;ListAccording=fieldDest;var len=ListAccording.length;for(var i=0;i<ListAvailable.length;i++)
{if((ListAvailable.options[i]!=null)&&(ListAvailable.options[i].selected))
{if(ListAvailable.options[i].getAttribute("blame")!=null)
{if(client_action)
{alert(ListAvailable.options[i].text+" "+_("cannot be choosen, because it doesn't have structure of scientific name definition."));}
continue;}
else
{ListAccording.options[len]=new Option(ListAvailable.options[i].text,ListAvailable.options[i].value);ListAccording.options[len].setAttribute("title",ListAvailable.options[i].getAttribute("title"));}
len++;ListAvailable.options[i]=null;i--;}}}
function moveOptionsUp(selectId)
{var selectList=document.getElementById(selectId);var selectOptions=selectList.getElementsByTagName('option');for(var i=1;i<selectOptions.length;i++)
{var opt=selectOptions[i];if(opt.selected)
{selectList.removeChild(opt);selectList.insertBefore(opt,selectOptions[i-1]);}}}
function moveOptionsDown(selectId)
{var selectList=document.getElementById(selectId);var selectOptions=selectList.getElementsByTagName('option');for(var i=selectOptions.length-2;i>=0;i--)
{var opt=selectOptions[i];if(opt.selected)
{var nextOpt=selectOptions[i+1];opt=selectList.removeChild(opt);nextOpt=selectList.replaceChild(opt,nextOpt);selectList.insertBefore(nextOpt,opt);}}}