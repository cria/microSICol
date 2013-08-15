
var multi_language_fields=new Array();multi_language_fields.push('coll_host_name');multi_language_fields.push('coll_substratum');multi_language_fields.push('coll_comments');multi_language_fields.push('cul_medium');multi_language_fields.push('cul_comments');multi_language_fields.push('iso_isolation_from');multi_language_fields.push('iso_method');multi_language_fields.push('ident_method');multi_language_fields.push('cha_ogm_comments');multi_language_fields.push('cha_biorisk_comments');multi_language_fields.push('cha_restrictions');multi_language_fields.push('cha_pictures');multi_language_fields.push('cha_urls');multi_language_fields.push('cha_catalogue');multi_language_fields.push('pro_properties');multi_language_fields.push('pro_applications');multi_language_fields.push('pro_urls');var default_multi_language_fields=new Array();default_multi_language_fields.concat(multi_language_fields);default_multi_language_fields.push('coll_host_name');default_multi_language_fields.push('coll_substratum');default_multi_language_fields.push('coll_comments');default_multi_language_fields.push('iso_isolation_from');default_multi_language_fields.push('iso_method');default_multi_language_fields.push('ident_method');default_multi_language_fields.push('cul_medium');default_multi_language_fields.push('cul_incub_time');default_multi_language_fields.push('cul_oxy_req');default_multi_language_fields.push('cul_comments');default_multi_language_fields.push('cha_ogm_comments');default_multi_language_fields.push('cha_biorisk_comments');default_multi_language_fields.push('cha_restrictions');default_multi_language_fields.push('cha_pictures');default_multi_language_fields.push('cha_urls');default_multi_language_fields.push('cha_catalogue');default_multi_language_fields.push('pro_properties');default_multi_language_fields.push('pro_applications');default_multi_language_fields.push('pro_urls');var mapTextArea=new Object();mapTextArea['taxon_ref']=65535;mapTextArea['ambient_risk']=65535;mapTextArea['hazard_group_ref']=65535;mapTextArea['comments']=65535;mapTextArea['synonym']=65535;mapTextArea['history']=65535;mapTextArea['extra_codes']=65535;mapTextArea['general_comments']=65535;mapTextArea['dep_preserv_method']=65535;mapTextArea['dep_aut_result']=65535;mapTextArea['dep_comments']=65535;mapTextArea['gps_comments']=65535;mapTextArea['coll_host_name_*']=65535;mapTextArea['coll_place']=65535;mapTextArea['coll_substratum_*']=65535;mapTextArea['coll_comments_*']=65535;mapTextArea['iso_isolation_from_*']=65535;mapTextArea['iso_method_*']=65535;mapTextArea['iso_comments']=65535;mapTextArea['ident_method_*']=65535;mapTextArea['ident_comments']=65535;mapTextArea['cul_medium_*']=65535;mapTextArea['cul_comments_*']=65535;mapTextArea['cha_biochemical']=65535;mapTextArea['cha_immunologic']=65535;mapTextArea['cha_morphologic']=65535;mapTextArea['cha_pathogenic']=65535;mapTextArea['cha_genotypic']=65535;mapTextArea['cha_ogm_comments_*']=65535;mapTextArea['cha_biorisk_comments_*']=65535;mapTextArea['cha_restrictions_*']=65535;mapTextArea['cha_pictures_*']=65535;mapTextArea['cha_urls_*']=65535;mapTextArea['cha_catalogue_*']=65535;mapTextArea['pro_properties_*']=65535;mapTextArea['pro_applications_*']=65535;mapTextArea['pro_urls_*']=65535;function validateStrains(dateformat)
{errors=false;form=document.getElementsByName('edit')[0];id_species=document.getElementsByName('id_species')[0];lbl_id_species=getLabel('id_species');id_division=document.getElementsByName('id_division')[0];lbl_id_division=getLabel('id_division');var code=document.getElementsByName('numeric_code')[0];lbl_code=getLabel('numeric_code');dep_date=document.getElementsByName('dep_date')[0];lbl_dep_date=getLabel('dep_date');dep_aut_date=document.getElementsByName('dep_aut_date')[0];lbl_dep_aut_date=getLabel('dep_aut_date');coll_date=document.getElementsByName('coll_date')[0];lbl_coll_date=getLabel('coll_date');coll_gps_latitude=document.getElementsByName('coll_gps_latitude')[0];lbl_coll_gps_latitude=getLabel('coll_gps_latitude');coll_gps_longitude=document.getElementsByName('coll_gps_longitude')[0];lbl_coll_gps_longitude=getLabel('coll_gps_longitude');coll_gps_precision=document.getElementsByName('coll_gps_precision')[0];lbl_coll_gps_precision=getLabel('coll_gps_precision');coll_global_code=document.getElementsByName('coll_global_code')[0];lbl_coll_global_code=getLabel('coll_global_code');coll_state_field=document.getElementsByName('coll_state')[0];lbl_coll_state_field=getLabel('coll_state');iso_date=document.getElementsByName('iso_date')[0];lbl_iso_date=getLabel('iso_date');ident_date=document.getElementsByName('ident_date')[0];lbl_ident_date=getLabel('ident_date');resetField(id_division,lbl_id_division);resetField(id_species,lbl_id_species);resetField(code,lbl_code);resetField(dep_date,lbl_dep_date);resetField(coll_date,lbl_coll_date);resetField(coll_gps_latitude,lbl_coll_gps_latitude);resetField(coll_gps_longitude,lbl_coll_gps_longitude);resetField(coll_gps_precision,lbl_coll_gps_precision);resetField(coll_global_code,lbl_coll_global_code);resetField(coll_state_field,lbl_coll_state_field);resetField(iso_date,lbl_iso_date);resetField(ident_date,lbl_ident_date);if(isEmpty(id_division,lbl_id_division))errors=true;if(isEmpty(code,lbl_code))errors=true;else if(!checkCode(code,lbl_code))errors=true;if(!checkGPS('latitude',coll_gps_latitude))errors=true;if(!checkGPS('longitude',coll_gps_longitude))errors=true;if(!checkPrecision(coll_gps_precision,lbl_coll_gps_precision))errors=true;if(!checkGlobalCode(coll_global_code,lbl_coll_global_code,'AAAA/AA/YYYY/\*'))errors=true;if(!checkState(coll_state_field,lbl_coll_state_field))errors=true;if(!isValidTextArea('history',65535))errors=true;if(!isValidTextArea('extra_codes',65535))errors=true;if(!isValidTextArea('general_comments',65535))errors=true;if(!checkValidDate(coll_date,lbl_coll_date,dateformat))errors=true;if(!checkValidDate(iso_date,lbl_iso_date,dateformat))errors=true;if(!isValidTextArea('dep_preserv_method',65535))errors=true;if(!checkValidDate(dep_date,lbl_dep_date,dateformat))errors=true;if(!checkValidDate(dep_aut_date,lbl_dep_aut_date,dateformat))errors=true;if(!isValidTextArea('dep_aut_result',65535))errors=true;if(!isValidTextArea('dep_comments',65535))errors=true;if(!isValidTextArea('gps_comments',65535))errors=true;if(!isValidTextArea('coll_place',65535))errors=true;if(!isValidTextArea('iso_comments',65535))errors=true;if(!checkValidDate(ident_date,lbl_ident_date,dateformat))errors=true;if(!isValidTextArea('ident_comments',65535))errors=true;if(!isValidTextArea('cha_biochemical',65535))errors=true;if(!isValidTextArea('cha_immunologic',65535))errors=true;if(!isValidTextArea('cha_morphologic',65535))errors=true;if(!isValidTextArea('cha_pathogenic',65535))errors=true;if(!isValidTextArea('cha_genotypic',65535))errors=true;langs=document.getElementById('data_langs').value;langs=langs.split(',');for(mlf=0;mlf<multi_language_fields.length;mlf++)
{max_size=mapTextArea[multi_language_fields[mlf]+'_*'];for(lang=0;lang<langs.length;lang++)
{if(!isValidTextArea(multi_language_fields[mlf]+'_'+langs[lang],max_size))errors=true;}}
if(isEmpty(id_species,lbl_id_species))errors=true;if(!checkOrderedDates(dateformat))errors=true;return errors;}
function init_combo()
{count_items=document.getElementById('coll_country').options.length;real_id=0;for(real_id=0;real_id<count_items;real_id++)
{if(document.getElementById('coll_country').options[real_id].value==selected_country)
{break;}}
document.getElementById('coll_country').selectedIndex=real_id;state_name=document.getElementById('coll_state').value;city_name=document.getElementById('coll_city').value;changeCountry(selected_country);changeState(selected_state);document.getElementById('coll_state').disabled=false;document.getElementById('coll_city').disabled=false;if(state_name!='')document.getElementById('coll_state').value=state_name;else if(selected_country==0)document.getElementById('coll_state').disabled=true;if(city_name!='')document.getElementById('coll_city').value=city_name;else document.getElementById('coll_city').disabled=true;}
function disableLinks()
{disableMenu(document.getElementById('menu'),document.getElementById('active_strains'));disableLink(document.getElementById('active_preferences'));disableLink(document.getElementById('active_configuration'));disableLink(document.getElementById('active_utilities'));}
addEvent(window,'load',init_combo);addEvent(window,'load',disableLinks);function onChangeState(obj)
{if(checkState(obj,null))changeStateByName(obj.value);else
{document.getElementById('coll_city').value='';document.getElementById('coll_city').disabled=true;}}
function isFloat(value,max_integers,max_decimals,signed)
{if(value.charAt(0)=='-')
{if(!signed)return false;value=value.substring(1);}
num_ints=0;num_decs=0;dot_read=false;for(i=0;i<value.length;i++)
{if(value.charAt(i)=='.')
{if(!dot_read)dot_read=true;else return false;continue;}
if(!isInteger(value.charAt(i)))return false;if(dot_read)num_decs++;else num_ints++;if(num_ints>max_integers)return false;if(num_decs>max_decimals)return false;}
return true;}
function checkFloat(obj,lbl_obj,max_integers,max_decimals,signed)
{if(lbl_obj==null)lbl_obj=getLabel(obj.id);if(obj.value!='')
{if(!isFloat(obj.value,max_integers,max_decimals,signed))
{warn=_("Out of format:")+' "';for(i=0;i<max_integers;i++)warn+='D';warn+='.';for(i=0;i<max_decimals;i++)warn+='D';warn+='" '+_("where D = digit.");if(!signed)warn+=" "+_("Positive values only.");showError(obj,lbl_obj,warn);return false;}
else
{resetField(obj,lbl_obj);return true;}}
else
{resetField(obj,lbl_obj);return true;}}
function checkPrecision(obj,lbl_obj)
{if(lbl_obj==null)lbl_obj=getLabel(obj.id);if(obj.value=="")
{resetField(obj,lbl_obj);return true;}
warn=_("Out of format:")+' "';warn+="DDDDD";warn+='" '+_("where D = digit.");warn+=" "+_("Positive values only.");if(!isInteger(obj.value))
{showError(obj,lbl_obj,warn);return false;}
if(obj.value.length<5)
{showError(obj,lbl_obj,warn);return false;}
resetField(obj,lbl_obj);return true;}
function isFormat(value,format)
{AZ="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";DIGIT="0123456789";get_any=false;current_index=0;year='';if(value.length==0)return false;while(current_index<value.length)
{if(!get_any)type=format.charAt(current_index);current_char=value.charAt(current_index);if(type=='A')
{if(AZ.indexOf(current_char)==-1)return false;}
else if(type=='Y')
{if(DIGIT.indexOf(current_char)==-1&&current_char!='X')return false;year+=current_char;}
else if(type=='/')
{if(current_char!='/')return false;if(format.charAt(current_index+1)=='*')
{if(!ValidYear(year)&&year!='XXXX')return false;else return true;}}
else return false;current_index++;}
if(current_index>=format.length)return true;else return false;}
function inRange(value,start,end)
{if(!isInteger(value))return false;value=value*1;if(value<start||value>end)return false;else return true;}
function checkRange(obj,lbl_obj,min,max)
{if(lbl_obj==null)lbl_obj=getLabel(obj.id);if(obj.value!='')
{if(!inRange(obj.value,min,max))
{showError(obj,lbl_obj,_("Value must be between")+' '+min+' '+_("and")+' '+max+'.');return false;}
else
{resetField(obj,lbl_obj);return true;}}
else
{resetField(obj,lbl_obj);return true;}}
function checkGlobalCode(obj,lbl_obj,format)
{if(lbl_obj==null)lbl_obj=getLabel(obj.id);if(obj.value!='')
{if(!isFormat(obj.value,format))
{showError(obj,lbl_obj,_("Out of format:")+' "'+format+'. '+_("Where: A = letter;YYYY = year;* = any character."));return false;}
else
{resetField(obj,lbl_obj);return true;}}
else
{resetField(obj,lbl_obj);return true;}}
function changeCountry(js_id_country)
{if(js_id_country==0)
{document.getElementById('coll_state').value='';document.getElementById('coll_state').disabled=true;document.getElementById('coll_city').value='';document.getElementById('coll_city').disabled=true;return;}
else document.getElementById('coll_state').disabled=false;var states=country_state[js_id_country];has_states=false;count_items=0;for(state in states)
{count_items++;if(count_items==2)
{has_states=true;break;}}
document.getElementById('coll_city').value='';document.getElementById('coll_city').disabled=true;ac_city.length=0;document.getElementById('coll_state').value='';ac_state.length=0;if(has_states)
{document.getElementById('coll_state').disabled=false;for(state in states)
{if(state=='name')continue;ac_state.push(states[state]);}}}
function checkState(obj,lbl_obj)
{if(lbl_obj==null)lbl_obj=getLabel(obj.id);if(obj.value!='')
{if(!obj.value.match(/\([A-Z0-9]{1,4}\)/))
{showError(obj,lbl_obj,_("Please add the state code according to the example: State Name (SN)."));return false;}
else
{resetField(obj,lbl_obj);return true;}}
else
{resetField(obj,lbl_obj);return true;}}
function changeState(js_id_state)
{var cities=state_city[js_id_state];for(city in cities)
{ac_city.push(cities[city]);}}
function changeStateByName(state_name)
{if(state_name=='')
{document.getElementById('coll_city').disabled=true;document.getElementById('coll_city').value='';return;}
var states=country_state[document.getElementById('coll_country').options[document.getElementById('coll_country').selectedIndex].value];document.getElementById('coll_city').disabled=false;document.getElementById('coll_city').value='';ac_city.length=0;id_of_the_state=-1;for(index in states)
{if(index=='name')continue;if(states[index]==state_name)id_of_the_state=index;}
if(id_of_the_state!=-1)changeState(id_of_the_state);}
function hideIfNewStrain()
{_next_action=document.getElementsByName('next_action')[0];if(_next_action&&_next_action.value=='insert')
{document.getElementById('tab_quality').style.display='none';document.getElementById('quality').style.display='none';document.getElementById('tab_stock').style.display='none';document.getElementById('stock').style.display='none';}}
function checkTaxonGroup()
{var sel=document.getElementById('id_species');var current_group=sel.options[sel.selectedIndex].getAttribute('group').toString();if(current_group=='5')
{document.getElementById('specific_for_protozoa').style.display="block";}
else
{document.getElementById('specific_for_protozoa').style.display="none";document.getElementById('coll_global_code').value="";if(document.getElementById('coll_clinical_form').length>0)document.getElementById('coll_clinical_form').selectedIndex=0;document.getElementById('hiv_unknown').checked=true;document.getElementById('hiv_yes').checked=false;document.getElementById('hiv_no').checked=false;}}
function checkOrderedDates(dateformat)
{var noerror=true;var input_colldate=document.getElementById('coll_date');var input_isodate=document.getElementById('iso_date');var input_identdate=document.getElementById('ident_date');var input_depdate=document.getElementById('dep_date');return noerror;}
function format_strain_code()
{numeric_code=parseInt($("#numeric_code").val(),10);if(isNaN(numeric_code))
{numeric_code=0;}
$("#code").html(sprintf(strain_format[$("#id_division").val()],numeric_code))}
addEvent(window,'load',hideIfNewStrain);addEvent(window,'load',checkTaxonGroup);