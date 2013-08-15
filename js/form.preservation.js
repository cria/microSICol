
var multi_language_fields=new Array();var temporaryPageLocations={};var temporaryPageOriginalLocations={};var exceptionLocations={};var default_multi_language_fields=new Array();default_multi_language_fields.concat(multi_language_fields);var mapTextArea=new Object();var strain_info=new Array();var msg='';$("<img>").attr("src","../img/loading.gif");$(document).ready(function(){for(var idStrain in strain_info){info=strain_info[idStrain];var locations=eval(info.current_locations);if(locations){for(var i=0;i<locations.length;i++){var loc=locations[i];if(!temporaryPageLocations[loc.id_container_hierarchy]){temporaryPageLocations[loc.id_container_hierarchy]={};}
temporaryPageLocations[loc.id_container_hierarchy][loc.row+"_"+loc.col]=loc;}}
if(info.origin_type=="lot"){parts=info.origin_location.split("_");if(!temporaryPageOriginalLocations[info.strain]){temporaryPageOriginalLocations[info.strain]={};}
if(!temporaryPageOriginalLocations[info.strain][parts[0]]){temporaryPageOriginalLocations[info.strain][parts[0]]={};};temporaryPageOriginalLocations[info.strain][parts[0]][parts[1]+"_"+parts[2]]={code:undefined,row:parts[1],col:parts[2],id_container:info.origin_container_id,id_container_hierarchy:parts[0],id_lot:info.id_lot,id_strain:info.strain,name:undefined,partial:(info.origin_decrease_stock=='y')};}}});function handleError(error,context){restoreOpenButton(context.counter);alert(error);}
function disableOriginControls(counter){$("#preservation_method").attr("disabled","disabled");$("#preservation_strain_"+counter).attr("disabled","disabled");$("#preservation_origin_"+counter).attr("disabled","disabled");$("#preservation_origin_lot_"+counter).attr("disabled","disabled");}
function originLocationUpdate(result,locationNames,extra){temporaryPageOriginalLocations[extra.idStrain]=result;disableOriginControls(extra.counter);var origin_location=undefined;for(container in result){origin_location=container+"_";for(loc in result[container]){origin_location+=loc;loc_data=result[container][loc];origin_location+='_'+loc_data.quantity;if(loc_data.partial!=undefined&&loc_data.partial=='y'){exceptionLocations[extra.idStrain]={};}
else{loc_parts=loc.split("_");exceptionLocations[extra.idStrain]={idContainerHierarchy:container,row:loc_parts[0],col:loc_parts[1]};}
break;}
break;}
$(extra.originLocationTextCtrl).val(locationNames);if(origin_location){$(extra.originLocationCtrl).val(origin_location);}}
function locationUpdate(result,locationNames,extra){$('#preservation_method').attr('disabled','disabled');if($('#preservation_origin_'+extra.counter).val()=='lot'){$('#preservation_origin_'+extra.counter).attr('disabled','disabled');$('#preservation_origin_lot_'+extra.counter).attr('disabled','disabled');$('#preservation_origin_location_text_'+extra.counter).attr('disabled','disabled');$('#preservation_origin_location_stock_'+extra.counter).attr('disabled','disabled');$('#img_source_'+extra.counter).hide();}
else{$('#preservation_origin_'+extra.counter).attr('disabled','disabled');}
temporaryPageLocations=result;extra.strainCombo.attr('disabled','disabled');var json=[];for(var idContainerHierarchy in temporaryPageLocations){for(var rowCol in temporaryPageLocations[idContainerHierarchy]){var item=temporaryPageLocations[idContainerHierarchy][rowCol];if(item.id_lot==extra.idLot&&item.id_strain==extra.idStrain){item.row=rowCol.split("_")[0];item.col=rowCol.split("_")[1];json[json.length]=item;}}}
extra.currentLocationsCtrl.val(JSON.stringify(json));extra.preparedCtrl.val(locationNames.length);extra.stockPositionCtrl.css('height',2+(locationNames.length*16)+"px");var str='';extra.stockPositionCtrl.removeOption(/./);for(var i=0;i<locationNames.length;i++){str+=locationNames[i]+'\n';extra.stockPositionCtrl.addOption(locationNames[i],locationNames[i]);}
extra.stockPositionHiddenCtrl.val(str);}
function resizeStockPos(){}
function checkUsedStrain(counter,idStrain){var result=true;$('.select_75').each(function(idx,obj){if(!($(obj).attr("id")=="preservation_strain")&&!($(obj).attr("id")=="preservation_strain_"+counter)){var curIdStrain=$(obj).val();if(curIdStrain==idStrain&&$(obj).attr('disabled')){alert(_('This strain is already in used in this preservation, please choose another strain.'));restoreOpenButton(counter);result=false;}}});return result;}
function restoreOpenButton(counter){img=$('img[counter='+counter+']');img.removeAttr('disabled');img.attr('src','../img/pick.png');}
function getExceptionLocations(){var exceptions=[];for(var idStrain in exceptionLocations){exceptions[exceptions.length]=exceptionLocations[idStrain];}
return exceptions;}
var openLocationPicker=function(imgId,operation,callbackFunction,_currentLocations){var imgSrc=$(imgId).attr('src');if(imgSrc=='../img/loading.gif'){return;}
$(imgId).attr('src','../img/loading.gif');var info=getInfo($(imgId),operation);if(info==undefined){return;}
var picker=new LocationPicker({operation:operation,idColl:info.idCollVal,idSubcoll:info.idSubcollVal,idPreservationMethod:info.idPreservationMethodVal,idStrain:info.idStrainVal,idLot:info.idLotVal,idOriginLot:info.idOriginLotVal,idStrain:info.idStrainVal,maxSelections:(operation=='remove'?1:-1),exceptionLocations:info.exceptionLocation,temporaryPageLocations:_currentLocations,callback:function(result,locationNames,extra){callbackFunction(result,locationNames,extra);},callbackInfo:{counter:info.counter,idLot:info.idLotVal,idStrain:info.idStrainVal,stockPositionHiddenCtrl:$("#preservation_stock_pos_"+info.counter),stockPositionCtrl:$("#preservation_stock_pos_select_"+info.counter),currentLocationsCtrl:$("#current_locations_"+info.counter),originLocationTextCtrl:$('#preservation_origin_location_text_'+info.counter),originLocationCtrl:$('#preservation_origin_location_'+info.counter),preparedCtrl:$("#preservation_prepared_"+info.counter),strainCombo:$('#preservation_strain_'+info.counter)},errorCallback:function(errorCode,context){handleError(errorCode,context);},errorCallbackInfo:{counter:info.counter}});var img=$(imgId);picker.display(function(){img.removeAttr('disabled');img.attr('src',imgSrc);});};function isTemporaryTarget(idContainerHierarchy,row,col){var temp=temporaryPageLocations[idContainerHierarchy];if(temp){return temp[row+"_"+col];}}
function getInfo(ctrl,operation){var counter=$(ctrl).attr('counter');var idStrainVal=$('#preservation_strain_'+counter).val();if(!(checkUsedStrain(counter,idStrainVal))){return;}
$(ctrl).attr('disabled','disabled');loading=true;var idLotVal=$('#id_lot').val();var idOriginLotVal=$('#preservation_origin_lot_'+counter).val();var idCollVal=$('#id_coll').val();var idSubcollVal=$('#id_subcoll').val();var idPreservationMethodVal=$('#preservation_method').val();if(!idLotVal){idLotVal=-(idStrainVal);}
if(operation=='add'){var incomingExceptionLocations=getExceptionLocations();var thisExceptionLocations=incomingExceptionLocations;}
return{counter:counter,idStrainVal:idStrainVal,idLotVal:idLotVal,idOriginLotVal:idOriginLotVal,idCollVal:idCollVal,idSubcollVal:idSubcollVal,idPreservationMethodVal:idPreservationMethodVal,exceptionLocation:thisExceptionLocations};}
function newStrain(Display){var icf=document.getElementById('invisible_clonable_fields');var os=document.getElementById('other_strains');var temp=icf.cloneNode(true);temp.id='strain';temp.style.display='block';renameFormElements(temp);os.appendChild(temp);filterLotNumber(document.getElementById('preservation_strain_'+global_counter),false);var obj=document.getElementById("preservation_method");var this_counter=global_counter;$('#preservation_stock_pos_select_'+global_counter).attr('disabled','true');$('#strain_'+global_counter).find('img.new').attr('counter',global_counter);$('#strain_'+global_counter).find('img.source').attr('counter',global_counter);$('#strain_'+global_counter).find('img.source').attr('id','img_source_'+global_counter);$('#strain_'+global_counter).find('img.source').css("display",Display);$('#strain_'+global_counter).find('img.new').click(function(){if($('#preservation_origin_'+this_counter).val()=='lot'&&(!$('#preservation_origin_location_text_'+this_counter).val())){alert(_('You need to select an original location before picking a destination location'));return;}
openLocationPicker($(this),'add',locationUpdate,temporaryPageLocations);});$('#strain_'+global_counter).find('img.source').click(function(){var counter=$(this).attr("counter");var id_strain=$("#preservation_strain_"+counter).val();if(isOriginReused(id_strain)){alert(_("This strain's origin location cannot be change because its reused by another strain in this preservation"));return;}
openLocationPicker($(this),'remove',originLocationUpdate,temporaryPageOriginalLocations[id_strain]);});$('#preservation_origin_lot_'+global_counter).change(function(){$('#preservation_origin_location_'+this_counter).val('');$('#preservation_origin_location_text_'+this_counter).val('');});filterLotNumber(document.getElementById('preservation_strain_'+global_counter),false);var obj=document.getElementById("preservation_method");tinyMCE.execCommand('mceAddControl',true,'preservation_macro_characs_'+global_counter);tinyMCE.execCommand('mceAddControl',true,'preservation_micro_characs_'+global_counter);tinyMCE.execCommand('mceAddControl',true,'preservation_result_'+global_counter);tinyMCE.execCommand('mceAddControl',true,'preservation_obs_'+global_counter);mapTextArea['preservation_macro_characs_'+global_counter]=65535;mapTextArea['preservation_micro_characs_'+global_counter]=65535;mapTextArea['preservation_result_'+global_counter]=65535;mapTextArea['preservation_obs_'+global_counter]=65535;if($.browser.msie&&$.browser.version=='6.0')
{var object=document.getElementById("minimize_strain_"+global_counter);MaximizeMinimize(object,'innerstrain_');MaximizeMinimize(object,'innerstrain_');}
global_counter++;return false;}
function changedOrigin(obj,reset){objNumber=String(obj.id);if(objNumber=="undefined"){obj=obj[0];objNumber=String(obj.id);}
objNumber=objNumber.substr(objNumber.lastIndexOf('_')+1);if(objNumber=="undefined")
{return;}
if(obj.selectedIndex==0){document.getElementById('origin_name_'+objNumber).style.display='block';document.getElementById('origin_lot_'+objNumber).style.display='none';document.getElementById('origin_lot_ampoules_'+objNumber).style.display='none';document.getElementById('origin_lot_ampoules_stock_'+objNumber).style.display='none';}
else if(obj.selectedIndex==1){document.getElementById('origin_name_'+objNumber).style.display='none';document.getElementById('origin_lot_'+objNumber).style.display='block';document.getElementById('origin_lot_ampoules_'+objNumber).style.display='block';document.getElementById('origin_lot_ampoules_stock_'+objNumber).style.display='block';document.getElementById('origin_lot_ampoules_stock_'+objNumber).style.display='block';$('origin_lot_ampoules_stock_'+objNumber).css('z-index',100);$('#preservation_origin_lot_'+objNumber).change();}}
function validatePreservation(dateformat){errors=false;lot=document.getElementsByName('preservation_lot')[0];lbllot=getLabel('preservation_lot');preserv_date=document.getElementsByName('preservation_date')[0];lbl_preserv_date=getLabel('preservation_date');responsible=document.getElementsByName('preservation_user')[0];lbl_responsible=getLabel('preservation_user');resetField(lot,lbllot);resetField(preserv_date,lbl_preserv_date);if(isEmpty(lot,lbllot))errors=true;if(isEmpty(preserv_date,lbl_preserv_date))
errors=true;else
if(!checkValidDate(preserv_date,lbl_preserv_date,dateformat))errors=true;if(isEmptySelect(responsible,lbl_responsible))errors=true;if(!isValidTextArea('preservation_process_data',65535))errors=true;for(var i=1;i<global_counter;i++)
{strain_select_id='#preservation_strain_'+i;if($(strain_select_id)[0].selectedIndex==-1)continue;if(!isValidTextArea('preservation_macro_characs_'+i,65535))errors=true;if(!isValidTextArea('preservation_micro_characs_'+i,65535))errors=true;if(!isValidTextArea('preservation_result_'+i,65535))errors=true;if(!isValidTextArea('preservation_obs_'+i,65535))errors=true;locations_id='#preservation_stock_pos_select_'+i;label_id='#label_preservation_stock_pos_select_'+i;if($(locations_id+' option').length<1){showError($(locations_id)[0],$(label_id)[0],_('You need to choose at least one stock position for this strain'));errors=true;}}
if(global_counter==1)
{alert(_("Please choose at least one strain."));errors=true;newStrain('none');isEmpty(document.getElementById('preservation_prepared_'+i,'label_preservation_prepared_'+i));isEmpty(document.getElementById('preservation_stock_limit_'+i,'label_preservation_stock_limit_'+i));}
else
{var num_of_strains=0;var chosen_strains=new Array();for(var i=1;i<global_counter;i++)
{sel=document.getElementById('preservation_strain_'+i);if(sel.length==0)continue;num_of_strains++;v=sel.options[sel.selectedIndex].value;sel_lbl=getLabel('label_preservation_strain_'+i);resetField(sel,sel_lbl);if(i>1)
{if(v in oc(chosen_strains))
{alert(_("Repeated Strain:")+' '+sel.options[sel.selectedIndex].text);showError(sel,sel_lbl,_("Repeated Strain"));errors=true;break;}}
chosen_strains.push(v);if(isEmpty(document.getElementById('preservation_stock_limit_'+i,'label_preservation_stock_limit_'+i)))errors=true;}
if(num_of_strains==0)
{alert(_("Please choose at least one strain."));errors=true;newStrain('none');isEmpty(document.getElementById('preservation_prepared_'+i,'label_preservation_prepared_'+i));}}
document.getElementById('global_counter_total').value=global_counter;document.getElementById('global_lot_strain_values').value=get_lot_strain_values(false);document.getElementById('new_combination').value=get_lot_strain_values(true);if(!errors)
{$('#preservation_method').removeAttr('disabled');for(var i=1;i<global_counter;i++)
{obj=document.getElementById('preservation_strain_'+i);obj.disabled=false;obj=document.getElementById('preservation_origin_'+i);obj.disabled=false;obj=document.getElementById('preservation_original_name_'+i);obj.disabled=false;obj=document.getElementById('preservation_origin_lot_'+i);obj.disabled=false;$('#preservation_origin_location_text_'+i).removeAttr('disabled');$('#preservation_origin_location_stock_'+i).removeAttr('disabled');$('img.source').show();}}
return errors;}
function get_lot_strain_values(compact_mode)
{var str=[];if(global_strain_lot!=null)
{for(var i=1;i<global_counter;i++)
{sel=document.getElementById('preservation_strain_'+i);if(sel.length==0)continue;strainID=sel.options[sel.selectedIndex].value;if(document.getElementById('preservation_origin_'+i).selectedIndex==1)
{sel=document.getElementById('preservation_origin_lot_'+i);lotID=sel.options[sel.selectedIndex].value;if(compact_mode)
{str.push(strainID+'-'+lotID);}
else
{if(global_strain_lot[strainID]!=undefined)
{if(global_strain_lot[strainID][lotID]!=undefined)
{maxAmpoules=global_strain_lot[strainID][lotID]['ampoules'];usedAmpoules=global_strain_lot[strainID][lotID]['used'];}
else
{maxAmpoules=0;usedAmpoules=0;}
str.push(strainID+'-'+lotID+'-'+maxAmpoules+'-'+usedAmpoules);}
else
{str.push(strainID+'-'+lotID);}}}
else if(compact_mode)
{str.push(strainID+'-0');}}}
return str.join(',');}
function disableLinks()
{disableMenu(document.getElementById('menu'),document.getElementById('active_preservation'));disableLink(document.getElementById('active_preferences'));disableLink(document.getElementById('active_configuration'));disableLink(document.getElementById('active_utilities'));}
function loadHiddenForm()
{if(document.getElementById('invisible_clonable_fields'))
{document.getElementById('invisible_clonable_fields').style.display='block';document.getElementById('invisible_clonable_fields').style.display='none';document.getElementById('invisible_clonable_fields').style.display='block';document.getElementById('invisible_clonable_fields').style.display='none';}}
function loadExtraForms()
{if(strain_info.length>0)
{$('#preservation_method').attr('disabled','disabled');for(var i=1;i<strain_info.length;i++)
{current_strain=strain_info[i];newStrain('none');obj=document.getElementById('preservation_strain_'+i);found=false;for(var j=0;j<obj.options.length;j++)
{if(obj.options[j].value==current_strain['strain']){obj.selectedIndex=j;found=true;}}
if(!found){var j=obj.options.length;obj.options[j]=new Option(current_strain['code']+' - '+current_strain['sciname_no_auth'],current_strain['strain']);obj.selectedIndex=j;}
obj.disabled=true;obj=document.getElementById('preservation_origin_'+i);if(current_strain['origin_type']=='original')
{obj.selectedIndex=0;obj.disabled=true;obj=document.getElementById('preservation_original_name_'+i);obj.value=current_strain['origin_info'];}
else if(current_strain['origin_type']=='lot')
{filterLotNumber(document.getElementById('preservation_strain_'+i),false);var preservation_origin_select=$('#preservation_origin_'+i);preservation_origin_select.removeOption(/./);var myOptions={"original":_("Original Culture"),"lot":_("Lot")};preservation_origin_select.addOption(myOptions,false);preservation_origin_select.selectOptions("lot");var preservation_origin_select_lot=$('#preservation_origin_lot_'+i);preservation_origin_select_lot.addOption(current_strain['id_lot'],current_strain['lot_name']);obj.disabled=true;document.getElementById('origin_name_'+i).style.display='none';document.getElementById('origin_lot_'+i).style.display='block';document.getElementById('origin_lot_ampoules_'+i).style.display='block';$('#preservation_origin_location_stock_'+i).css("display","inline");$('#preservation_origin_location_'+i).val(current_strain['origin_location']);$('#preservation_origin_location_text_'+i).val(current_strain['origin_location_text']);$('#origin_lot_ampoules_stock_'+i).css('display','block');obj=document.getElementById('preservation_origin_lot_'+i);for(var j=0;j<obj.options.length;j++){if(obj.options[j].value==current_strain['id_lot'])
obj.selectedIndex=j;}
obj.disabled=true;}
$('#preservation_stock_pos_'+i).val(current_strain['stock_pos_str']);$('#preservation_stock_pos_select_'+i).addOption(current_strain['stock_pos'],false);obj=document.getElementById('preservation_prepared_'+i);obj.value=current_strain['prepared'];obj=document.getElementById('preservation_stock_limit_'+i);obj.value=current_strain['stock_minimum'];obj=document.getElementById('current_locations_'+i);obj.value=current_strain['current_locations'];obj=document.getElementById('preservation_culture_medium_'+i);for(var j=0;j<obj.options.length;j++)
{if(obj.options[j].value==current_strain['culture_medium'])obj.selectedIndex=j;}
obj=document.getElementById('preservation_temp_'+i);obj.value=current_strain['temp'];obj=document.getElementById('preservation_incub_time_'+i);obj.value=current_strain['incub_time'];obj=document.getElementById('preservation_cryo_'+i);obj.value=current_strain['cryo'];obj=document.getElementById('preservation_type_'+i);for(var j=0;j<obj.options.length;j++)
{if(obj.options[j].value==current_strain['preservation_type'])obj.selectedIndex=j;}
obj=document.getElementById('preservation_purity_'+i);if(current_strain['purity']=='y')obj.selectedIndex=0;else obj.selectedIndex=1;obj=document.getElementById('preservation_counting_'+i);obj.value=current_strain['counting'];obj=document.getElementById('preservation_counting_na_'+i);if(current_strain['counting_na']=='y')obj.checked=true;else obj.checked=false;obj=document.getElementById('preservation_macro_characs_'+i);obj.value=current_strain['macro'];obj=document.getElementById('preservation_micro_characs_'+i);obj.value=current_strain['micro'];obj=document.getElementById('preservation_result_'+i);obj.value=current_strain['result'];obj=document.getElementById('preservation_obs_'+i);obj.value=current_strain['obs'];setTimeout("updateLater("+i+")",100);for(var j=0;j<reused_strains.length;j++){if($('#preservation_strain_'+i).val()==reused_strains[j]){$('#delete_strain_'+i).click(function(){return false;});$('#delete_strain_'+i+' img').attr('title',_("This strain cannot be removed because it has been used as origin of another preservation, a quality control or a distribution."));console.debug("hiding image");$('img.new[counter='+i+']').hide();}}}
resizeStockPos();}}
function updateLater(i)
{obj=document.getElementById('minimize_strain_'+i);MaximizeMinimize(obj,'innerstrain_');}
function limitAmpoules(obj,prepared_field)
{numberOnly(obj);var ThisNumber=obj.id.substr(obj.id.lastIndexOf('_')+1);sel=document.getElementById('preservation_strain_'+ThisNumber);var currentStrain=sel.options[sel.selectedIndex].value;if(prepared_field)
{var currentLot=document.getElementById('preservation_lot').getAttribute('lot_id');}
else
{sel=document.getElementById('preservation_origin_lot_'+ThisNumber);var currentLot=sel.options[sel.selectedIndex].value;}
var total_amp=0;if(global_strain_lot!=null&&global_strain_lot[currentStrain]!=undefined&&global_strain_lot[currentStrain][currentLot]!=undefined)total_amp=global_strain_lot[currentStrain][currentLot]['ampoules']*1;if(prepared_field)
{var prepared_amp=obj.value*1;var prep_old_amp=0;if(global_strain_lot!=null&&global_strain_lot[currentStrain]!=undefined&&global_strain_lot[currentStrain][currentLot]!=undefined)prep_old_amp=global_strain_lot[currentStrain][currentLot]['prepared']*1;total_amp=prep_old_amp-total_amp;if(prepared_amp<total_amp)
{alert(_("Exceeded minimum amount of existing ampoules. Switching to minimum allowed value."));obj.value=total_amp;}}
else
{var used_amp=obj.value*1;var prev_used_amp=0;if(global_strain_lot[currentStrain][currentLot])prev_used_amp=global_strain_lot[currentStrain][currentLot]['used']*1;total_amp+=prev_used_amp;if(used_amp>total_amp)
{alert(_("Exceeded maximum amount of existing ampoules. Switching to maximum allowed value."));obj.value=total_amp;}}}
function filterLotNumber(sel,reset)
{if(global_strain_lot!=null)
{var currentStrain=sel.options[sel.selectedIndex].value;var ThisNumber=sel.id.substr(sel.id.lastIndexOf('_')+1);$('#preservation_origin_location_'+ThisNumber).val('');$('#preservation_origin_location_text_'+ThisNumber).val('');lot_sel=document.getElementById('preservation_origin_lot_'+ThisNumber);if(global_strain_lot[currentStrain]==undefined)
{var preservation_origin_select=$('#preservation_origin_'+ThisNumber);preservation_origin_select.removeOption(/./);var myOptions={"original":_("Original Culture")};preservation_origin_select.addOption(myOptions,false);preservation_origin_select.selectOptions("original")
changedOrigin(preservation_origin_select,reset);}
else
{var preservation_origin_select=$('#preservation_origin_'+ThisNumber);preservation_origin_select.removeOption(/./);var myOptions={"original":_("Original Culture"),"lot":_("Lot")};preservation_origin_select.addOption(myOptions,false);preservation_origin_select.selectOptions("original")
changedOrigin(preservation_origin_select,reset);}
lot_sel.length=0;for(var lot_opt in global_strain_lot[currentStrain])
{lot_sel.options[lot_sel.length]=new Option(global_strain_lot[currentStrain][lot_opt]['name'],lot_opt);lot_sel.options[lot_sel.length-1].setAttribute("unit",global_strain_lot[currentStrain][lot_opt]['unit_measure']);}
if(lot_sel&&lot_sel.length==0)
{$("#preservation_origin_"+ThisNumber).removeOption("lot");$("#preservation_origin_"+ThisNumber).selectOptions("original")
changedOrigin($("#preservation_origin_"+ThisNumber),reset);}}}
function removeStrainFromTemp(div){var counter=$(div).attr("id").split("_")[1];var idLotVal=$('#id_lot').val();var idStrainVal=$('#preservation_strain_'+counter).val();for(var idContainerHierarchy in temporaryPageLocations){var locations=temporaryPageLocations[idContainerHierarchy];for(var rowCol in locations){var loc=locations[rowCol];if(loc&&loc.id_strain==idStrainVal&&((!idLotVal)||Math.abs(loc.id_lot)==idLotVal)){delete temporaryPageLocations[idContainerHierarchy][rowCol];}}}
delete temporaryPageOriginalLocations[idStrainVal];delete exceptionLocations[idStrainVal];}
function isOriginReused(idStrain){var originForStrain=temporaryPageOriginalLocations[idStrain];if(!originForStrain){return false;}
for(var idContainerHierarchy in temporaryPageLocations){for(var rowCol in temporaryPageLocations[idContainerHierarchy]){var item=temporaryPageLocations[idContainerHierarchy][rowCol];var originForContainer=originForStrain[item.id_container_hierarchy];if(originForContainer&&originForContainer[rowCol]){if(item.id_strain!=idStrain){return true;}}}}
return false;}
function removeStrain(obj){var ctrlId=$(obj).attr("id");var id=ctrlId.split("_");id=id[id.length-1];var target_strain_id=$('#preservation_strain_'+id).val();if(isOriginReused(target_strain_id)){alert(_("This strain cannot be removed because its origin location is reused by another strain in this preservation"));return;}
if((reused_strains!=undefined)&&(reused_strains!=null)){for(i=0;i<reused_strains.length;i++){if(target_strain_id==reused_strains[i]){alert(_("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."));return;}}}
if((not_identified_strains!=undefined)&&(not_identified_strains!=null)){for(i=0;i<not_identified_strains.length;i++){if(target_strain_id==not_identified_strains[i]){alert(_("This preservation can not be deleted because it has been used as origin of another preservation, a quality control, a distribution, or a stock movement."));return;}}}
objpar=obj.parentNode;objpar.parentNode.style.display='none';removeStrainFromTemp(objpar.parentNode);for(var i=0;i<objpar.childNodes.length;i++)
{if(objpar.childNodes[i].nodeType==1&&objpar.childNodes[i].tagName.toUpperCase()=='SELECT')
{objpar.childNodes[i].length=0;}}}
addEvent(window,'load',disableLinks);addEvent(window,'load',loadHiddenForm);addEvent(window,'load',loadExtraForms);