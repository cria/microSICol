
var temporaryPageLocations={};$(document).ready(function(){if(location.href.indexOf('.new.')>-1){$('#distribution_lot').change(function()
{$('#distribution_quantity').val('');$('#distribution_locations').removeOption(/./);});$('#distribution_strain').change(function()
{$('#distribution_quantity').val('');$('#distribution_locations').removeOption(/./);});setupLocation('#distribution_strain','#distribution_lot',temporaryPageLocations,window);filterLotNumber(true);}
else{filterLotNumber(true);$('img.source').hide();$('#distribution_strain').attr('disabled','disabled');if(distribution_data!=null){$('#distribution_lot').addOption(distribution_data[0],distribution_data[1]);}
$('#distribution_lot').attr('disabled','disabled');}});function callbackFunction(result,locationNames,extra){temporaryPageLocations=result;$('#distribution_quantity').val(locationNames.length);var locations_data="";for(id_container_hierarchy in result){container_contents=result[id_container_hierarchy];for(row_col in container_contents){location_def=container_contents[row_col];if(locations_data.length>0){locations_data+="|";}
var parts=row_col.split('_');var row=parts[0];var col=parts[1];locations_data+=location_def.id_container_hierarchy+";"+
row+";"+col+";"+location_def.quantity;}}
$('#locations_data').val(locations_data);var locations_sel=$('#distribution_locations');locations_sel.removeOption(/./);for(var i=0;i<locationNames.length;i++){locations_sel.addOption(i,locationNames[i]);}}
var multi_language_fields=new Array();var default_multi_language_fields=new Array();default_multi_language_fields.concat(multi_language_fields);var mapTextArea=new Object();function validateDistribution(dateformat)
{$('#distribution_strain').removeAttr('disabled');$('#distribution_lot').removeAttr('disabled');errors=false;date=document.getElementsByName('distribution_date')[0];lbl_date=getLabel('distribution_date');tech=document.getElementsByName('distribution_user')[0];lbl_tech=getLabel('distribution_user');quantity=document.getElementsByName('distribution_quantity')[0];lbl_quantity=getLabel('distribution_quantity');resetField(date,lbl_date);resetField(tech,lbl_tech);resetField(quantity,lbl_quantity);if(!checkValidDate(date,lbl_date,dateformat))errors=true;else if(isEmpty(date,lbl_date))errors=true;if(isEmpty(quantity,lbl_quantity))errors=true;if(isEmpty(tech,lbl_tech))errors=true;if(!isValidTextArea('distribution_reason',65535))errors=true;if($('#distribution_locations')[0].options.length==0)
{showError($('#distribution_locations')[0],$('#label_distribution_locations')[0],_('You need to choose at least one stock position'));errors=true;}
if(document.getElementById('distribution_lot').value=='')errors=true;else if(location.href.indexOf('.new.')>-1)document.getElementById("global_lot_strain_values").value=get_lot_strain_values();if(errors&&$('#distribution_locations')[0].options.length>0)
{$('#distribution_strain').attr('disabled','true');$('#distribution_lot').attr('disabled','true');}
return errors;}
function disableLinks()
{disableMenu(document.getElementById('menu'),document.getElementById('active_distribution'));disableLink(document.getElementById('active_preferences'));disableLink(document.getElementById('active_configuration'));disableLink(document.getElementById('active_utilities'));}
function filterPeopleOnInstitution(idElementInst,idElementPeople)
{var cmbInst=document.getElementById(idElementInst);var idInst=cmbInst.options[cmbInst.selectedIndex].value.toString();var cmbPeople=document.getElementById(idElementPeople);var selectedPerson=0;if(cmbPeople.selectedIndex!=0)
{selectedPerson=cmbPeople.options[cmbPeople.selectedIndex].value;}
if(!cmbPeople.innerOptions)
{cmbPeople.innerOptions=new Array();for(var i=1;i<cmbPeople.length;i++)
{cmbPeople.innerOptions[i]=new Array(cmbPeople.options[i].text,cmbPeople.options[i].value,cmbPeople.options[i].getAttribute('inst').toString());}}
cmbPeople.options.length=0;cmbPeople.options[0]=new Option('---','');for(var i=1;i<cmbPeople.innerOptions.length;i++)
{var InstPeople=cmbPeople.innerOptions[i][2].split("|");var IsPeopleOnInstitution=false;var j=0;while(j<InstPeople.length&&!IsPeopleOnInstitution)
{if(InstPeople[j]==idInst)IsPeopleOnInstitution=true;j++;}
if(IsPeopleOnInstitution)
{cmbPeople.options[cmbPeople.options.length]=new Option(cmbPeople.innerOptions[i][0],cmbPeople.innerOptions[i][1]);}}
if(selectedPerson>0)
{for(var i=0;i<cmbPeople.options.length;i++)
{if(cmbPeople.options[i].value==selectedPerson)
{cmbPeople.selectedIndex=i;break;}}}}
function limitAmpoules(obj)
{if(document.getElementById('distribution_lot').options[0].value!='')
{numberOnly(obj);var ThisNumber=obj.id.substr(obj.id.lastIndexOf('_')+1);sel=document.getElementById('distribution_strain');var currentStrain=sel.options[sel.selectedIndex].value;sel=document.getElementById('distribution_lot');var currentLot=sel.options[sel.selectedIndex].value;var used_amp=obj.value*1;var total_amp=global_strain_lot[currentStrain][currentLot]['ampoules']*1;var prev_used_amp=global_strain_lot[currentStrain][currentLot]['used']*1;total_amp+=prev_used_amp;if(used_amp>total_amp)
{alert(_("Exceeded maximum amount of existing ampoules. Switching to maximum allowed value."));obj.value=total_amp;}}}
function filterLotNumber(isInit)
{if(global_strain_lot!=null)
{var sel=document.getElementById('distribution_strain');var currentStrain=sel.options[sel.selectedIndex].value;var lot_sel=document.getElementById('distribution_lot');lot_sel.length=0;if(global_strain_lot[currentStrain]==undefined)
{lot_sel.options[lot_sel.length]=new Option("","");$("#img_source").attr("style","display: none");if(!isInit)
{alert(_("There are no Lot Numbers for this Strain."));}
return;}else
{$("#img_source").attr("style","display: inline");}
for(var lot_opt in global_strain_lot[currentStrain])
{lot_sel.options[lot_sel.length]=new Option(global_strain_lot[currentStrain][lot_opt]['name'],lot_opt);}}}
function get_lot_strain_values()
{var str=[];if(global_strain_lot!=null)
{var sel=document.getElementById('distribution_strain');var strainID=sel.options[sel.selectedIndex].value;var lot_sel=document.getElementById('distribution_lot');for(var i=0;i<lot_sel.options.length;i++)
{lotID=lot_sel.options[i].value;if(global_strain_lot[strainID][lotID]==undefined)continue;maxAmpoules=global_strain_lot[strainID][lotID]['ampoules'];usedAmpoules=global_strain_lot[strainID][lotID]['used'];str.push(strainID+'-'+lotID+'-'+maxAmpoules+'-'+usedAmpoules);}}
return str.join(',');}
function init()
{addEvent(document.getElementById('distribution_strain'),'change',function(e){filterLotNumber(false)});addEvent(document.getElementById('distribution_quantity'),'keyup',function(e){numberOnly(document.getElementById('distribution_quantity'))});addEvent(document.getElementById('distribution_quantity'),'blur',function(e){limitAmpoules(document.getElementById('distribution_quantity'))});}
addEvent(window,'load',init);addEvent(window,'load',disableLinks);