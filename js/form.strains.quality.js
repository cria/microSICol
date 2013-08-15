
var temporaryPageLocations={};$(document).ready(function(){if(location.href.indexOf('.new.')>-1){setupLocation('#id_strain','#lot',temporaryPageLocations,parent.window,function(){if(!$('#lot').val()){alert(_('Please select an origin lot before choosing the origin location'));return false;}
return true;});}
else{$('img.source').hide();$('#lot').attr('disabled','disabled');$('#quality_stock_decrease').attr('disabled','disabled');$('#lot').attr('disabled','disabled');}});function callbackFunction(result,locationNames,extra){console.debug("Result: %o LocationNames: %o",result,locationNames);temporaryPageLocations=result;$('#num_amp').val(locationNames.length);var locations_data="";for(id_container_hierarchy in result){container_contents=result[id_container_hierarchy];for(row_col in container_contents){location_def=container_contents[row_col];if(locations_data.length>0){locations_data+="|";}
var parts=row_col.split('_');var row=parts[0];var col=parts[1];locations_data+=location_def.id_container_hierarchy+";"+
row+";"+col+";"+location_def.quantity;}}
$('#locations_data').val(locations_data);var locations_sel=$('#quality_locations');console.debug("Sel: %o",locations_sel);locations_sel.removeOption(/./);for(var i=0;i<locationNames.length;i++){locations_sel.addOption(i,locationNames[i]);}}
var mapTextAreaQuality=new Object();function newQualityTest()
{var icf=document.getElementById('invisible_clonable_fields');var os=document.getElementById('other_quality_tests');var temp=icf.cloneNode(true);temp.id='quality_test';temp.style.display='block';renameFormElements(temp);os.appendChild(temp);document.getElementById('test_'+global_counter).onblur=function(){isEmptySelect(this);};tinyMCE.execCommand('mceAddControl',true,'result_'+global_counter);mapTextAreaQuality['result_'+global_counter]=65535;tinyMCE.execCommand('mceAddControl',true,'comments_'+global_counter);mapTextAreaQuality['comments_'+global_counter]=65535;global_counter++;resizeIframe();return false;}
function loadHiddenForm()
{document.getElementById('invisible_clonable_fields').style.display='block';document.getElementById('invisible_clonable_fields').style.display='none';document.getElementById('invisible_clonable_fields').style.display='block';document.getElementById('invisible_clonable_fields').style.display='none';}
function showQuality()
{if(window.frames['ifrm_quality'])
{if(document.location.toString().indexOf("detail")>-1)type="detail";else type="other";window.frames['ifrm_quality'].location="strains.quality.list.py?type="+type+"&id="+document.forms[0].id.value;}}
function cancelEdit()
{document.location="strains.quality.list.py?type=other&id="+document.getElementById("id_strain").value;}
function validateStrainQuality(dateformat)
{$('#lot').removeAttr('disabled');$('#quality_stock_decrease').removeAttr('disabled');errors=false;date=document.getElementsByName('date')[0];lbl_date=getLabel('date');tec_resp=document.getElementsByName('tec_resp')[0];lbl_tec_resp=getLabel('tec_resp');num_amp=document.getElementsByName('num_amp')[0];lbl_num_amp=getLabel('label_quality_locations');lot=document.getElementsByName('lot')[0];lbl_lot=getLabel('lot');resetField(date,lbl_date);resetField(num_amp,lbl_num_amp);if(isEmpty(date,lbl_date))errors=true;else if(!checkValidDate(date,lbl_date,dateformat))errors=true;if(isEmptySelect(tec_resp))errors=true;if(isEmpty(num_amp,lbl_num_amp)){errors=true;}else{if((num_amp.value*1)<=0&&$('#quality_locations')[0].options[0].value!="NI"){$('#lot').attr('disabled','disabled');$('#quality_stock_decrease').attr('disabled','disabled');alert(_("The number of ampoules must be greater than zero."));num_amp.focus();return;}}
if(isEmptySelect(lot))errors=true;var num_of_tests=0;for(var i=1;i<global_counter;i++)
{if(document.getElementById('test_'+i).length==0)continue;if(isEmptySelect(document.getElementById('test_'+i)))errors=true;if(!isValidTextArea('result_'+i,65535))errors=true;if(!isValidTextArea('comments_'+i,65535))errors=true;num_of_tests++;}
if(num_of_tests==0)
{Feedback(-4);resizeIframe();return;}
document.getElementById('global_counter_total').value=global_counter;document.getElementById('global_lot_strain_values').value=get_lot_strain_values(document.getElementById('id_strain').value);if(!errors)
{Feedback(0);document.forms['edit'].submit();}
else
{$('#lot').attr('disabled','disabled');$('#quality_stock_decrease').attr('disabled','disabled');Feedback(-1);resizeIframe();}}
function loadExtraForms()
{if(test_info.length>0)
{for(var i=1;i<test_info.length;i++)
{current_test=test_info[i];newQualityTest();obj=document.getElementById('test_'+i);for(var j=0;j<obj.options.length;j++)
{if(obj.options[j].value==current_test['id_test'])obj.selectedIndex=j;}
obj=document.getElementById('purity_'+i);if(current_test['purity']=='y')obj.selectedIndex=0;else obj.selectedIndex=1;obj=document.getElementById('counting_'+i);obj.value=current_test['counting'];obj=document.getElementById('counting_not_apply_'+i);if(current_test['counting_not_apply']=='y')obj.checked=true;else obj.checked=false;obj=document.getElementById('result_'+i);obj.value=current_test['result'];obj=document.getElementById('comments_'+i);obj.value=current_test['comments'];setTimeout("updateLater("+i+")",100);}}}
function updateLater(i)
{obj=document.getElementById('minimize_test_'+i);maximizeMinimize(obj,'inner_quality_test_');}
function maximizeMinimize(obj,prefix)
{MaximizeMinimize(obj,prefix);resizeIframe();return false;}
function resizeIframe()
{if(document.location.toString().indexOf("list")>-1)new_size=document.getElementById("quality_table").offsetHeight;else new_size=document.getElementById("general").offsetHeight;fr=window.parent.document.getElementById("ifrm_quality");fr.style.height=new_size+"px";}
function deleteQuality(id_strain,id_quality)
{document.location="strains.quality.save.py?action=delete&id_strain="+id_strain+"&id_quality="+id_quality;}
function filterLotNumber()
{var currentStrain=document.getElementById('id_strain').value;lot_sel=document.getElementById('lot');lot_sel.length=0;lot_sel.options[lot_sel.length]=new Option("","");if(global_strain_lot!=null)
{for(var lot_opt in global_strain_lot[currentStrain])
{lot_sel.options[lot_sel.length]=new Option(global_strain_lot[currentStrain][lot_opt]['name'],lot_opt);lot_sel.options[lot_sel.length-1].setAttribute("unit",global_strain_lot[currentStrain][lot_opt]['unit_measure']);if(lot_sel.options[lot_sel.length-1].value==document.getElementById("id_lot_old").value)
{lot_sel.options[lot_sel.length-1].selected=true;}}}
else
{if(location.href.indexOf('.new.')>-1){alert(_("There are no Lot Numbers for this Strain."));}
else
{if(quality_data!=null)
{$('#lot').addOption(quality_data[0],quality_data[1]);}}
return;}}
function limitAmpoules(obj,id_strain)
{if(isEmpty(obj,document.getElementById("label_num_amp")))return;var currentStrain=id_strain;sel=document.getElementById('lot');var currentLot=sel.options[sel.selectedIndex].value;if(global_strain_lot!=null&&sel.selectedIndex!=0)
{numberOnly(obj);var used_amp=obj.value*1;if(used_amp<=0)
{alert(_("The number of ampoules must be greater than zero."));obj.value="";obj.focus();return;}
var total_amp=global_strain_lot[currentStrain][currentLot]['ampoules']*1;var prev_used_amp=global_strain_lot[currentStrain][currentLot]['used']*1;total_amp+=prev_used_amp;if(used_amp>total_amp)
{alert(_("Exceeded maximum amount of existing ampoules. Switching to maximum allowed value."));obj.value=total_amp;}}}
function resetAmpoules()
{document.getElementById("num_amp").value="";$('#quality_locations').removeOption(/./);}
function get_lot_strain_values(id_strain)
{var str=[];if(global_strain_lot!=null)
{strainID=id_strain;sel=document.getElementById('lot');for(var i=1;i<sel.options.length;i++)
{lotID=sel.options[i].value;maxAmpoules=global_strain_lot[strainID][lotID]['ampoules'];usedAmpoules=global_strain_lot[strainID][lotID]['used'];str.push(strainID+'-'+lotID+'-'+maxAmpoules+'-'+usedAmpoules);}}
return str.join(',');}
function removeTest(obj)
{objpar=obj.parentNode;objpar.parentNode.style.display='none';for(var i=0;i<objpar.childNodes.length;i++)
{if(objpar.childNodes[i].nodeType==1&&objpar.childNodes[i].tagName.toUpperCase()=='SELECT')
{objpar.childNodes[i].length=0;}}
resizeIframe();}
function disableLinks()
{window.parent.document.getElementById("href_save_submit").value=window.parent.document.getElementById("save_submit").href;window.parent.document.getElementById("href_cancel_submit").value=window.parent.document.getElementById("cancel_submit").href;window.parent.document.getElementById("save_submit").href="#";window.parent.document.getElementById("cancel_submit").href="#";window.parent.document.getElementById("tab_general").href="#";window.parent.document.getElementById("tab_deposit").href="#";window.parent.document.getElementById("tab_coll_event").href="#";window.parent.document.getElementById("tab_isolation").href="#";window.parent.document.getElementById("tab_identification").href="#";window.parent.document.getElementById("tab_culture").href="#";window.parent.document.getElementById("tab_characs").href="#";window.parent.document.getElementById("tab_properties").href="#";window.parent.document.getElementById("tab_quality").href="#";window.parent.document.getElementById("tab_stock").href="#";window.parent.document.getElementById("tab_security").href="#";var color="#CCCCC0";window.parent.document.getElementById("save_record").src="../img/record_save_disabled.png";window.parent.document.getElementById("cancel_record").src="../img/record_cancel_disabled.png";window.parent.document.getElementById("tab_general").style.color=color;window.parent.document.getElementById("tab_deposit").style.color=color;window.parent.document.getElementById("tab_coll_event").style.color=color;window.parent.document.getElementById("tab_isolation").style.color=color;window.parent.document.getElementById("tab_identification").style.color=color;window.parent.document.getElementById("tab_culture").style.color=color;window.parent.document.getElementById("tab_characs").style.color=color;window.parent.document.getElementById("tab_properties").style.color=color;window.parent.document.getElementById("tab_quality").style.color=color;window.parent.document.getElementById("tab_stock").style.color=color;window.parent.document.getElementById("tab_security").style.color=color;}
function enableLinks()
{if(window.parent.document.getElementById("href_save_submit")!=null)
{if(window.parent.document.getElementById("href_save_submit").value!="")
{window.parent.document.getElementById("save_submit").href=window.parent.document.getElementById("href_save_submit").value;window.parent.document.getElementById("cancel_submit").href=window.parent.document.getElementById("href_cancel_submit").value;window.parent.document.getElementById("tab_general").href="javascript:show('general');";window.parent.document.getElementById("tab_deposit").href="javascript:show('deposit');";window.parent.document.getElementById("tab_coll_event").href="javascript:show('coll_event');";window.parent.document.getElementById("tab_isolation").href="javascript:show('isolation');";window.parent.document.getElementById("tab_identification").href="javascript:show('identification');";window.parent.document.getElementById("tab_culture").href="javascript:show('culture');";window.parent.document.getElementById("tab_characs").href="javascript:show('characs');";window.parent.document.getElementById("tab_properties").href="javascript:show('properties');";window.parent.document.getElementById("tab_quality").href="javascript:show('quality');showQuality();";window.parent.document.getElementById("tab_stock").href="javascript:show('stock');showStock();";window.parent.document.getElementById("tab_security").href="javascript:show('security');";window.parent.document.getElementById("save_record").src="../img/record_save.png";window.parent.document.getElementById("cancel_record").src="../img/record_cancel.png";window.parent.document.getElementById("tab_general").style.color="";window.parent.document.getElementById("tab_deposit").style.color="";window.parent.document.getElementById("tab_coll_event").style.color="";window.parent.document.getElementById("tab_isolation").style.color="";window.parent.document.getElementById("tab_identification").style.color="";window.parent.document.getElementById("tab_culture").style.color="";window.parent.document.getElementById("tab_characs").style.color="";window.parent.document.getElementById("tab_properties").style.color="";window.parent.document.getElementById("tab_quality").style.color="";window.parent.document.getElementById("tab_stock").style.color="";window.parent.document.getElementById("tab_security").style.color="";window.parent.document.getElementById("href_save_submit").value="";window.parent.document.getElementById("href_cancel_submit").value="";}}}
function applyTextUnitMeasure()
{var obj=document.getElementById("lot");if(obj.length>1)
{var target_label_used=document.getElementById("label_num_amp");if(obj.selectedIndex>0)
{if(target_label_used!=null)target_label_used.innerHTML=_("Number of Used %s").replace("%s",obj.options[obj.selectedIndex].getAttribute("unit"));}
else
{if(target_label_used!=null)target_label_used.innerHTML="";}}}