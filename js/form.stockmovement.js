
var temporaryPageLocations={};var temporaryPageOriginalLocations={};var exceptionLocations={};var exceptionOriginalLocations={};function validateStockMovement(dateformat){errors=false;date=document.getElementsByName('date')[0];lbl_date=getLabel('date');description=document.getElementsByName('description')[0];lbl_description=getLabel('description');resetField(date,lbl_date);resetField(description,lbl_description);if(isEmpty(date,lbl_date))
errors=true;else
if(!checkValidDate(date,lbl_date,dateformat))errors=true;if(isEmpty(description,lbl_description))errors=true;var has_stock_positions=false;var chosen_origin_positions=new Array();var chosen_destination_positions=new Array();for(var i=1;i<global_counter;i++)
{origin=document.getElementById('stockmovement_origin_location_'+i);origin_text=document.getElementById('stockmovement_origin_location_text_'+i);destination=document.getElementById('stockmovement_destination_location_'+i);destination_text=document.getElementById('stockmovement_destination_location_text_'+i);if(origin==null||origin==undefined)continue;if(origin.parentNode.parentNode.style.display=='none')continue;has_stock_positions=true;resetField(origin_text,null);if(origin.value=="")
{showError(origin_text,null,_("Field must not be empty."));$(origin_text).removeAttr("disabled")
$(origin_text).attr("readonly","readonly")
errors=true;}
else
{if(i>1)
{if(origin.value in oc(chosen_origin_positions))
{showError(origin_text,null,_("Repeated stock position."));$(origin_text).removeAttr("disabled")
$(origin_text).attr("readonly","readonly")
errors=true;}}
chosen_origin_positions.push(origin.value);}}
for(var i=1;i<global_counter;i++)
{destination=document.getElementById('stockmovement_destination_location_'+i);destination_text=document.getElementById('stockmovement_destination_location_text_'+i);if(destination==null||destination==undefined)continue;if(destination.parentNode.parentNode.style.display=='none')continue;resetField(destination_text,null);if(destination.value=="")
{continue;}
else
{if(destination.value in oc(chosen_origin_positions)||destination.value in oc(chosen_destination_positions))
{showError(destination_text,null,_("Repeated stock position."));$(destination_text).removeAttr("disabled")
$(destination_text).attr("readonly","readonly")
errors=true;}
chosen_destination_positions.push(destination.value);}}
if(!has_stock_positions)
alert(_("Please choose at least one stock position."))
document.getElementById('global_counter_total').value=global_counter;if(!errors)
$('#preservation_method').removeAttr('disabled');return errors;}
function removeStockMovement(obj){var ctrlId=$(obj).attr("id");var id=ctrlId.split("_");counter=id[id.length-1];objpar=obj.parentNode.parentNode;if($("#table_locations > tbody > tr:visible").length>1)
objpar.style.display='none';$(objpar).find('#stockmovement_origin_location_'+counter).val("");$(objpar).find('#stockmovement_origin_location_text_'+counter).val("");$(objpar).find('#stockmovement_destination_location_'+counter).val("");$(objpar).find('#stockmovement_destination_location_text_'+counter).val("");delete temporaryPageOriginalLocations[counter];delete temporaryPageLocations[counter];delete exceptionLocations[counter];delete exceptionOriginalLocations[counter];}
function newStockMovement(position_data){var icf=document.getElementById('invisible_clonable_fields');var table_loc=document.getElementById('table_locations');var temp=icf.cloneNode(true);temp.id='stock_movement';temp.style.display='';renameFormElements(temp);table_loc.tBodies[0].appendChild(temp);if(position_data)
{$('#stock_movement_'+global_counter).find('#stockmovement_origin_location_'+global_counter).val(position_data["origin_location"]);$('#stock_movement_'+global_counter).find('#stockmovement_origin_location_text_'+global_counter).val(position_data["origin_location_text"]);$('#stock_movement_'+global_counter).find('#stockmovement_destination_location_'+global_counter).val(position_data["destination_location"]);$('#stock_movement_'+global_counter).find('#stockmovement_destination_location_text_'+global_counter).val(position_data["destination_location_text"]);}
else
{$('#stock_movement_'+global_counter).find('img.new').attr('counter',global_counter);$('#stock_movement_'+global_counter).find('img.source').attr('counter',global_counter);var counter=$('#stock_movement_'+global_counter).find('img.new').attr('counter');$('#stock_movement_'+global_counter).find('img.source').click(function(){openLocationPicker($(this),'remove',originLocationUpdate,temporaryPageOriginalLocations[counter]);});$('#stock_movement_'+global_counter).find('img.new').click(function(){openLocationPicker($(this),'add',locationUpdate,temporaryPageLocations[counter]);});}
global_counter++;return false;}
function getExceptionLocations(){var exceptions=[];for(var counter in exceptionLocations){exceptions[exceptions.length]=exceptionLocations[counter];}
return exceptions;}
function getExceptionOriginalLocations(){var exceptions=[];for(var counter in exceptionOriginalLocations){exceptions[exceptions.length]=exceptionOriginalLocations[counter];}
return exceptions;}
function getInfo(ctrl,operation){var counter=$(ctrl).attr('counter');var idStrainVal=0;$(ctrl).attr('disabled','disabled');loading=true;var idLotVal=0;var idOriginLotVal=0;var idCollVal=0;var idSubcollVal=$('#id_subcoll').val();var idPreservationMethodVal=$('#preservation_method').val();if(operation=='add')
{var incomingExceptionLocations=getExceptionLocations();var thisExceptionLocations=incomingExceptionLocations;}
else
{var incomingExceptionOriginalLocations=getExceptionOriginalLocations();var thisExceptionOriginalLocations=incomingExceptionOriginalLocations;}
return{counter:counter,idStrainVal:idStrainVal,idLotVal:idLotVal,idOriginLotVal:idOriginLotVal,idCollVal:idCollVal,idSubcollVal:idSubcollVal,idPreservationMethodVal:idPreservationMethodVal,exceptionLocation:thisExceptionLocations,exceptionOriginalLocation:thisExceptionOriginalLocations};}
function originLocationUpdate(result,locationNames,extra){temporaryPageOriginalLocations[extra.counter]=result;disableOriginControls();var origin_location=undefined;for(container in result){origin_location=container+"_";for(loc in result[container]){origin_location+=loc;loc_data=result[container][loc];loc_parts=loc.split("_");exceptionOriginalLocations[extra.counter]={idContainerHierarchy:container,row:loc_parts[0],col:loc_parts[1]};break;}
break;}
$(extra.originLocationTextCtrl).val(locationNames);if(origin_location){$(extra.originLocationCtrl).val(origin_location);}
$(extra.originLocationTextCtrl).blur();}
function locationUpdate(result,locationNames,extra){temporaryPageLocations[extra.counter]=result;disableOriginControls();var destination_location=undefined;for(container in result){destination_location=container+"_";for(loc in result[container]){destination_location+=loc;loc_data=result[container][loc];loc_parts=loc.split("_");exceptionLocations[extra.counter]={idContainerHierarchy:container,row:loc_parts[0],col:loc_parts[1]};break;}
break;}
$(extra.destinationLocationTextCtrl).val(locationNames);if(destination_location){$(extra.destinationLocationCtrl).val(destination_location);}}
var openLocationPicker=function(imgId,operation,callbackFunction,_currentLocations){var imgSrc=$(imgId).attr('src');if(imgSrc=='../img/loading.gif'){return;}
$(imgId).attr('src','../img/loading.gif');var info=getInfo($(imgId),operation);if(info==undefined){return;}
$('#stockmovement_origin_location_text_'+info.counter).removeAttr("readonly")
$('#stockmovement_origin_location_text_'+info.counter).attr("disabled","disabled")
$('#stockmovement_destination_location_text_'+info.counter).removeAttr("readonly")
$('#stockmovement_destination_location_text_'+info.counter).attr("disabled","disabled")
var picker=new LocationPicker({operation:operation,module:"stock_movement",idColl:info.idCollVal,idSubcoll:info.idSubcollVal,idPreservationMethod:info.idPreservationMethodVal,idStrain:info.idStrainVal,idLot:info.idLotVal,idOriginLot:info.idOriginLotVal,idStrain:info.idStrainVal,maxSelections:1,exceptionLocations:info.exceptionLocation,exceptionOriginalLocations:info.exceptionOriginalLocation,temporaryPageLocations:_currentLocations,callback:function(result,locationNames,extra){callbackFunction(result,locationNames,extra);},callbackInfo:{counter:info.counter,idLot:info.idLotVal,idStrain:info.idStrainVal,originLocationTextCtrl:$('#stockmovement_origin_location_text_'+info.counter),originLocationCtrl:$('#stockmovement_origin_location_'+info.counter),destinationLocationTextCtrl:$('#stockmovement_destination_location_text_'+info.counter),destinationLocationCtrl:$('#stockmovement_destination_location_'+info.counter)},errorCallback:function(errorCode,context){handleError(errorCode,context);},errorCallbackInfo:{counter:info.counter}});var img=$(imgId);picker.display(function(){img.removeAttr('disabled');img.attr('src',imgSrc);});};function handleError(error,context){restoreOpenButton(context.counter);alert(error);}
function restoreOpenButton(counter){img=$('img.source');img.removeAttr('disabled');img.attr('src','../img/pick.png');}
function disableOriginControls(){$("#preservation_method").attr("disabled","disabled");}
function loadStockPositions()
{if(positions_info.length>0)
{for(var i=0;i<positions_info.length;i++)
{newStockMovement(positions_info[i]);}}
else
{newStockMovement();}}
addEvent(window,'load',loadStockPositions);