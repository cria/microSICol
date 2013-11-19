
if(!("console"in window)||!("firebug"in console)){var names=["log","debug","info","warn","error","assert","dir","dirxml","group","groupEnd","time","timeEnd","count","trace","profile","profileEnd"];window.console={};for(var i=0;i<names.length;++i)window.console[names[i]]=function(){};}
jQuery.fn.addFormattedOptions=function(rawArray,formatting){return this.each(function(i,control){if($(control).is('select')){var options='';$(rawArray).each(function(j,val){var value=val[formatting.value];var text=val[formatting.text];options+='<option value="'+value+'">'+text+'</option>';});$(control).html(options);}});};jQuery.fn.rotateToggle=function(){var pos=-1;for(var i=0;i<arguments.length;i++){if(arguments[i]){if($(this).is('.'+arguments[i])){pos=i;break;}}}
if(pos==-1){pos=0;}
var new_pos=pos+1;if(new_pos>arguments.length){new_pos=0;}
if(arguments[pos]){$(this).toggleClass(arguments[pos]);}
if(arguments[new_pos]){$(this).toggleClass(arguments[new_pos]);}
return this;};function setupLocation(id_strain_selector,id_lot_selector,temporary_loc,window_handler,pre_validation){$('img.source').click(function(){$('general').css('display','none');if(pre_validation){if(!pre_validation()){return;}}
var imgSrc=$(this).attr('src');if(imgSrc=='../img/loading.gif'){return;}
$(this).attr('src','../img/loading.gif');var picker=new window_handler.LocationPicker({operation:'remove',maxSelections:-1,idColl:$('#id_coll').val(),idSubcoll:$('#id_subcoll').val(),idStrain:$(id_strain_selector).val(),idOriginLot:$(id_lot_selector).val(),temporaryPageLocations:temporaryPageLocations,callback:function(result,locationNames,extra){callbackFunction(result,locationNames,extra);},callbackInfo:{}});var img=$(this);picker.display(function(){img.removeAttr('disabled');img.attr('src',imgSrc);});});}
Array.prototype.remove=function(from,to){var rest=this.slice((to||from)+1||this.length);this.length=from<0?this.length+from:from;return this.push.apply(this,rest);};function LocationPicker(data)
{this.idColl=data.idColl;this.idSubcoll=data.idSubcoll;this.idPreservationMethod=data.idPreservationMethod;this.idLot=data.idLot;this.idOriginLot=data.idOriginLot;this.idStrain=data.idStrain;this.strainCode=data.strainCode;this.strainName=data.strainName;this.operation=data.operation;this.maxSelections=data.maxSelections;this.onComplete=data.callback;this.extraInfo=data.callbackInfo;this.onLocationError=data.errorCallback;this.errorAdditionalInfo=data.errorCallbackInfo;this.exceptionLocations=data.exceptionLocations;this.exceptionOriginalLocations=data.exceptionOriginalLocations;this.module=data.module;if(!this.exceptionLocations){this.exceptionLocations={};}
if(!this.exceptionOriginalLocations){this.exceptionOriginalLocations={};}
this.removing=(this.operation=='remove');delete this.body;delete this.mainDialog;delete this.currentLocations;if(!this.idLot){this.idLot=-(this.idStrain);}
this.usedLocations={};this.temporaryPageLocations=cloneObject(data.temporaryPageLocations);this.currentLocations={};var that=this;this.ajaxStarted=function(img){img.show();};this.ajaxStopped=function(img){img.hide();};this.saveClicked=function(btn){this.save();};this.containerChanged=function(sel){this.initLocations(sel.val());};this.locationSelected=function(td,hierarchy,click){var row=td.attr('locRow');var col=td.attr('locCol');var quantity_total=td.attr('quantity_total');var quantity_used=td.attr('quantity_used');if(quantity_used==undefined){quantity_used=0;}
if(this.operation=='add'){if(click){td.addClass("selectedCell");}else{td.addClass("selectedCell");}}else{if(click){td.addClass("selectedCell");}else{td.addClass("selectedCell");}}
if(this.operation=='add')
{if(td.is(".selectedCell")||td.is(".selectedCellDist")){quantity_used=parseInt(quantity_used,10);if(click)
{if(isNaN($("#txtQtdClick").val()))
{quantity_used+=parseInt($("#txtQtdClick").val(),10);}
else
{quantity_used+=1;$("#txtQtdClick").val("1")}}
else
{quantity_used+=1;}
td.attr('quantity_used',quantity_used);this.addSelectedLocation(hierarchy,row,col,quantity_used);td.css('background-image',"url('../img/inserting.gif')");td.css('background-repeat','no-repeat');td.css('background-position','center');td.css('background-color','#C3C3C3');td.css('color','#FFFFFF');td.attr('title',_('Selected'));if(this.module!="stock_movement")
td.html(quantity_used);}}
else
{if(td.is(".selectedCell")){quantity_total=parseInt(quantity_total,10);quantity_used=parseInt(quantity_used,10);if(quantity_used+1<=quantity_total){if(this.module!="stock_movement")
quantity_used+=1;else
quantity_used=quantity_total;td.attr('quantity_used',quantity_used);this.addSelectedLocation(hierarchy,row,col,quantity_used,quantity_total);}
if(quantity_used>=quantity_total){td.css('background-image',"url('../img/removing.gif')");td.attr('title',_('Removed'));td.html('');}else{td.attr('title',_('Removed'));td.html((quantity_total-quantity_used));}}}
this.updateSave();};this.updateSave=function(){if(isEmptyObject(this.currentLocations)){$('#saveConfirm').attr("src","../img/record_save_disabled.png");$('#saveConfirm').css('cursor','default');$("#saveConfirm").unbind("click");}
else{$('#saveConfirm').attr("src","../img/record_save.png");$('#saveConfirm').css('cursor','pointer');$("#saveConfirm").click(function(){that.saveClicked($(this));});}};this.display=function(onCompleteCallback){if(this.operation=='add'){var action='main';var boxy_title=_('stock input');}
else{var action='remove_main';var boxy_title=_('stock output');}
$.ajaxSetup({async:false});$.get("location.callback.py",{action:action,id_strain:this.idStrain,id_coll:this.idColl,id_subcoll:this.idSubcoll,id_lot:this.idLot,id_origin_lot:this.idOriginLot,id_preservation_method:this.idPreservationMethod,currentLocations:JSON.stringify(this.currentLocations),random:Math.floor(Math.random()*1000001)},function(data,textStatus){if(data.error){if(that.onLocationError){that.onLocationError(data.error,that.errorAdditionalInfo);}}
else
{buildDialog(data,onCompleteCallback,boxy_title);}},'json');};this.save=function(){this.ajaxStarted($('#loading',this.getBody()));if(this.module=="stock_movement")
this.temporaryPageLocations=[];for(var idContainerHierarchy in this.temporaryPageLocations){var locations=this.temporaryPageLocations[idContainerHierarchy];for(var rowCol in locations){var loc=locations[rowCol];if(loc&&loc.id_strain==this.idStrain&&loc.id_lot==this.idLot){delete this.temporaryPageLocations[idContainerHierarchy][rowCol];}}}
for(var idContainerHierarchy in this.currentLocations){var locations=this.currentLocations[idContainerHierarchy];if(!this.temporaryPageLocations){this.temporaryPageLocations={};}
if(!this.temporaryPageLocations[idContainerHierarchy]){this.temporaryPageLocations[idContainerHierarchy]={};}
for(var i=0;i<locations.length;i++){var loc=locations[i];var key=idContainerHierarchy+'_'+loc.row+"_"+loc.col;this.temporaryPageLocations[idContainerHierarchy][loc.row+"_"+loc.col]={row:0,col:0,quantity:loc.quantity,id_strain:this.idStrain,id_lot:this.idLot,id_container:loc.id_container,id_container_hierarchy:idContainerHierarchy,code:undefined,name:undefined,partial:(loc.quantity<loc.quantity_total)?'y':'n'};}}
$.ajaxSetup({async:false});var locationNames=[];var divs=$('td.locationSummaryArea > div.containerHierarchy',this.getBody());for(var i=0;i<divs.length;i++){locationNames[locationNames.length]=$(divs[i]).text();}
this.mainDialog.unload();if(this.onComplete){this.onComplete(this.temporaryPageLocations,locationNames,this.extraInfo);}
$.ajaxSetup({async:true});this.mainDialog.hideAndUnload();if($('#distribution_strain').length)
{$('#distribution_strain')[0].disabled=true;$('#distribution_lot')[0].disabled=true;}
else
{if($('#ifrm_quality').length)
ifrm_quality.$("#lot")[0].disabled=true;}};this.getBody=function(){if(!this.mainDialog){return undefined;}
return this.mainDialog.getContent();};this.getIdContainerHierarchy=function(){return this.getSelectedContainerHierarchy();};this.getIdContainer=function(){return $('select.container',this.getBody()).val();};this.getContainer=function(){var id=parseInt(this.getIdContainerHierarchy(),10);var ret=undefined;$(this.containers).each(function(i,obj){if(parseInt(obj.id_container,10)==id){ret=obj;}});return ret;};this.addSelectedLocation=function(hierarchy,row,col,quantity_used,quantity_total){var idContainerHierarchy=hierarchy.id_container_hierarchy;var table=$('table.locationSummary',this.getBody());var td=$('td.locationSummaryArea',this.getBody());var div=$('<div></div>');div.addClass('containerHierarchy');div.addClass('containerHierarchy'+idContainerHierarchy);div.css('white-space','nowrap');div.css('padding-bottom','3px');div.hide();var rowCol=this.getContainerRowCol(idContainerHierarchy,row,col);table.queue(function(){var img=$('<img src="../img/remove.png" width="12px" height="12px" />');img.css('vertical-align','text-bottom');img.css('cursor','pointer');img.click(function(){that.removeSelectedLocation(hierarchy,row,col);if(idContainerHierarchy==that.getSelectedContainerHierarchy()){getLocations(hierarchy);}})
var content;if(that.module!="stock_movement")
content=" "+hierarchy.hierarchy+" "+rowCol+" ("+quantity_used+")";else
content=" "+hierarchy.hierarchy+" "+rowCol;var id=hierarchy.hierarchy+" "+row+"_"+col;var id=id.replace(/ /g,"_");var currentDiv=$("#"+id,this);if(!currentDiv||currentDiv.length<1){div.html(content);div.attr("id",id);div.appendTo(td);currentDiv=div;}
else{currentDiv.html(content);}
currentDiv.prepend(img);currentDiv.fadeIn('normal');table.dequeue();});this.markSelections(idContainerHierarchy);var position={row:row,col:col,quantity:quantity_used,quantity_total:quantity_total,id_container:hierarchy.id_container,div:div};if(!this.currentLocations){this.currentLocations={};}
if(this.currentLocations[idContainerHierarchy]){var idx=this.currentLocations[idContainerHierarchy].length;for(var i=0;i<this.currentLocations[idContainerHierarchy].length;i++){var loc=this.currentLocations[idContainerHierarchy][i];if(loc.col==col&&loc.row==row&&loc.id_container==hierarchy.id_container){idx=-1;loc.quantity=quantity_used;td.attr('quantity_used',loc.quantity);}}
if(idx>-1){this.currentLocations[idContainerHierarchy][idx]=position;}}
else{this.currentLocations[idContainerHierarchy]=[position];}};this.removeSelectedLocation=function(hierarchy,row,col){var idContainerHierarchy=hierarchy.id_container_hierarchy;var table=$('table.locationSummary',this.getBody());if(this.currentLocations&&this.currentLocations[idContainerHierarchy]){for(var i=0;i<this.currentLocations[idContainerHierarchy].length;i++){var l=this.currentLocations[idContainerHierarchy][i];if(l.row==row&&l.col==col){var currentDiv=this.currentLocations[idContainerHierarchy][i].div;table.queue(function(){currentDiv.slideUp('slow',function(){currentDiv.remove();});table.dequeue();});this.currentLocations[idContainerHierarchy].remove(i);if(this.currentLocations[idContainerHierarchy].length<1){delete this.currentLocations[idContainerHierarchy];this.updateSave();break;}}}}
if(this.temporaryPageLocations&&this.temporaryPageLocations[idContainerHierarchy]){var l=this.temporaryPageLocations[idContainerHierarchy];for(var rowCol in l){if(row+"_"+col==rowCol){delete this.temporaryPageLocations[idContainerHierarchy][rowCol];break;}}}};this.getCurrentLocation=function(idContainerHierarchy,row,col){col=parseInt(col,10);row=parseInt(row,10);if(this.currentLocations&&this.currentLocations[idContainerHierarchy]){var locs=this.currentLocations[idContainerHierarchy];for(var i=0;i<locs.length;i++){var loc=locs[i];if(parseInt(loc.row,10)==row&&parseInt(loc.col,10)==col){return loc;}}}
return undefined;};this.isThis=function(idLot,idStrain){return parseInt(this.idLot,10)==parseInt(idLot,10)&&parseInt(this.idStrain,10)==parseInt(idStrain,10);};this.isCurrentlySelected=function(idContainerHierarchy,row,col){if(this.getCurrentLocation(idContainerHierarchy,row,col)){return true;}
return false;};this.CurrentlyQuantity=function(idContainerHierarchy,row,col){var loc=this.getCurrentLocation(idContainerHierarchy,row,col);if(loc){return loc.quantity;}else{return 0;}}
this.getTemporaryLocation=function(idContainerHierarchy,row,col){locs=this.temporaryPageLocations;if(locs&&locs[idContainerHierarchy]&&locs[idContainerHierarchy][row+"_"+col]){return locs[idContainerHierarchy][row+"_"+col];}
return undefined;};this.isTemporaryLocation=function(idContainerHierarchy,row,col,idLot){var loc=this.getTemporaryLocation(idContainerHierarchy,row,col);if(idLot){return(loc&&loc.id_lot&&loc.id_lot==idLot);}
else{if(loc){return true;}
else{return false;}}};this.TemporaryQuantity=function(idContainerHierarchy,row,col,idLot){var loc=this.getTemporaryLocation(idContainerHierarchy,row,col);if(idLot){if(loc&&loc.id_lot&&loc.id_lot==idLot){return loc.quantity;}
else{return 0;}}
else{if(loc){return loc.quantity;}
else{return 0;}}}
this.getExceptionLocation=function(idContainerHierarchy,row,col){if(!this.exceptionLocations){return undefined;}
for(var i=0;i<this.exceptionLocations.length;i++){var loc=this.exceptionLocations[i];if(loc&&loc.idContainerHierarchy==idContainerHierarchy&&loc.row==row&&loc.col==col){return loc;}}
return undefined;};this.isExceptionLocation=function(idContainerHierarchy,row,col){var loc=this.getExceptionLocation(idContainerHierarchy,row,col);if(loc){return true;}
else{return false;}};this.getExceptionOriginalLocation=function(idContainerHierarchy,row,col){if(!this.exceptionOriginalLocations){return undefined;}
for(var i=0;i<this.exceptionOriginalLocations.length;i++){var loc=this.exceptionOriginalLocations[i];if(loc&&loc.idContainerHierarchy==idContainerHierarchy&&loc.row==row&&loc.col==col){return loc;}}
return undefined;};this.isExceptionOriginalLocation=function(idContainerHierarchy,row,col){var loc=this.getExceptionOriginalLocation(idContainerHierarchy,row,col);if(loc){return true;}
else{return false;}};this.getDatabaseLocation=function(idContainerHierarchy,row,col){var locs=this.usedLocations;if(locs&&locs[idContainerHierarchy]&&locs[idContainerHierarchy][row+"_"+col]){return locs[idContainerHierarchy][row+"_"+col];}
return undefined;};this.isDatabaseLocation=function(idContainerHierarchy,row,col,idLot){var loc=this.getDatabaseLocation(idContainerHierarchy,row,col);if(idLot){return(loc&&loc.id_lot&&loc.id_lot==idLot);}
else{if(loc){return true;}
else{return false;}}};this.isOurSelection=function(idContainerHierarchy,row,col){return this.isDatabaseLocation(idContainerHierarchy,row,col,this.idLot)||this.isTemporaryLocation(idContainerHierarchy,row,col,this.idLot);};this.getSelectedContainerHierarchy=function(){var currentSelect=undefined;var currentLevel=-1;$('select.location').each(function(){var css=$(this).attr('class').split(' ');for(var i=0;i<css.length;i++){if(css[i].indexOf("level_")>-1){var level=css[i].charAt(6);if(parseInt(level,10)>currentLevel){currentSelect=this;currentLevel=parseInt(level,10);}}}});return $(currentSelect).val();};this.createLocationSelects=function(){var hierarchy=this.hierarchy;$(this.containers).each(function(i,thisContainer){var thisHierarchy=hierarchy[thisContainer.id_container];hierarchy[thisContainer.id_container]=createOptions(thisHierarchy);});this.hierarchy=hierarchy;};this.markSelections=function(idContainerHierarchy){$('div.containerHierarchy',that.getBody()).css('color','#D0D0D0');$('div.containerHierarchy'+idContainerHierarchy,that.getBody()).css('color','black');};this.getRowCol=function(row,col){return row+"_"+col;};this.getContainerRowCol=function(idContainer,row,col){var locationSettings=that.locationSettings[idContainer];var iniRow=locationSettings.ini_row;var iniCol=locationSettings.ini_col;var pattern=locationSettings.pattern;return pattern.replace("%(row)s",getLabel(iniRow,row)).replace("%(col)s",getLabel(iniCol,col));};function createOptions(h,level){if(!level){level=1;}
$(h).each(function(i,obj){if(that.operation=='add'||obj.loc_count>0){var option='<option value="'+obj.id_container_hierarchy+'">'+obj.description+'</option>';h[i]['option']=option;h[i]['level']=level;that.hierarchyMap[obj.id_container][obj.id_container_hierarchy]['option']=option;that.hierarchyMap[obj.id_container][obj.id_container_hierarchy]['level']=level;if(obj.children){createOptions(obj.children,level+1);}}});return h;};this.initLocations=function(idContainer){$('select.location').remove();createCombos(this.hierarchy[idContainer]);};this.formatCell=function(cell,hierarchyPart,x,y){if(this.operation=='add'){this.formatAddCell(cell,hierarchyPart,x,y);}else if(this.operation=='remove'){this.formatRemoveCell(cell,hierarchyPart,x,y);}};this.clearMessage=function(callback){$('div.message').fadeOut(callback);};this.message=function(msg){$('div.message').html(_(msg));$('div.message').fadeIn();};this.formatRemoveCell=function(cell,hierarchyPart,x,y){var containsStrain=this.isDatabaseLocation(hierarchyPart.id_container_hierarchy,y,x);var isCurrentlySelected=this.isCurrentlySelected(hierarchyPart.id_container_hierarchy,y,x);var isTemporarySelected=this.isTemporaryLocation(hierarchyPart.id_container_hierarchy,y,x);var available;if(this.module!="stock_movement")
{available=containsStrain;}
else
{available=containsStrain&&(!this.isExceptionOriginalLocation(hierarchyPart.id_container_hierarchy,y,x)||isTemporarySelected);}
if(available){var item=this.getDatabaseLocation(hierarchyPart.id_container_hierarchy,y,x);cell.attr('quantity_total',item.available_qt);cell.attr('quantity_used','0');cell.css('background-image',"url('../img/inserting.gif')");cell.css('background-repeat','no-repeat');cell.css('background-position','center');cell.css('color','#FFFFFF');if(this.module!="stock_movement")
cell.html(item.available_qt);cell.hover(function(){$(this).css('cursor','pointer');},function(){$(this).css('cursor','default');});if(isCurrentlySelected||isTemporarySelected){var curQuantity=this.CurrentlyQuantity(hierarchyPart.id_container_hierarchy,y,x);var temQuantity=this.TemporaryQuantity(hierarchyPart.id_container_hierarchy,y,x);var max=(curQuantity>temQuantity)?curQuantity:temQuantity;for(i=1;i<=max;i++){this.locationSelected(cell,hierarchyPart);}}
cell.click(function(){var c=$(this);that.clearMessage(function(){if(c.is('.selectedCell')||c.is(".selectedCellDist")){that.locationSelected(c,hierarchyPart,true);}
else{var selectedTotal=$('.containerHierarchy').length;if(that.maxSelections>-1&&selectedTotal>that.maxSelections-1){that.message(_('You can select a maximum of [maxSelections] location, please deselect one before continuing.').replace('[maxSelections]',that.maxSelections));}else{that.locationSelected(c,hierarchyPart,true);}}});});}
else{cell.addClass('unav_location');}};this.formatAddCell=function(cell,hierarchyPart,x,y){var isCurrentlySelected=this.isCurrentlySelected(hierarchyPart.id_container_hierarchy,y,x);var isDatabaseSelected=this.isDatabaseLocation(hierarchyPart.id_container_hierarchy,y,x);var isTemporarySelected=this.isTemporaryLocation(hierarchyPart.id_container_hierarchy,y,x);force_un=false;if(this.isExceptionLocation(hierarchyPart.id_container_hierarchy,y,x)){isCurrentlySelected=false;isDatabaseSelected=false;if(this.module=="stock_movement")
var force_un=!isTemporarySelected;}
if(isTemporarySelected){isDatabaseSelected=false;var item=this.getTemporaryLocation(hierarchyPart.id_container_hierarchy,y,x);}else if(isDatabaseSelected){var item=this.getDatabaseLocation(hierarchyPart.id_container_hierarchy,y,x);}else{var item=undefined;}
var isUnavailable=(item&&!this.isThis(item.id_lot,item.id_strain))||force_un;if(isUnavailable){cell.addClass('unav_location');cell.html('<img class="unavailable" src="../img/inserting.gif">');}
else{cell.addClass('locationSelect');cell.hover(function(){$(this).css('cursor','pointer');},function(){$(this).css('cursor','default');});cell.click(function(){if(that.module!="stock_movement")
{that.locationSelected($(this),hierarchyPart,true);}
else
{var selectedTotal=$('.containerHierarchy').length;if(that.maxSelections>-1&&selectedTotal>that.maxSelections-1){that.message(_('You can select a maximum of [maxSelections] location, please deselect one before continuing.').replace('[maxSelections]',that.maxSelections));}else{that.locationSelected($(this),hierarchyPart,true);}}});if(isCurrentlySelected||isTemporarySelected){var curQuantity=this.CurrentlyQuantity(hierarchyPart.id_container_hierarchy,y,x);var temQuantity=this.TemporaryQuantity(hierarchyPart.id_container_hierarchy,y,x);var max=(curQuantity>temQuantity)?curQuantity:temQuantity;for(i=1;i<=max;i++){this.locationSelected(cell,hierarchyPart);}}}};function createCombos(thisHierarchy,parent){if(!parent){var level=1;}
else{var level=that.hierarchyMap[parent.id_container][parent.id_container_hierarchy].level+1;}
var i=level;while(true){var ctrlList=$('select.level_'+i,that.getBody());if(ctrlList.length<1){break;}
ctrlList.remove();}
var options='';$(thisHierarchy).each(function(i,obj){var option=that.hierarchyMap[obj.id_container][obj.id_container_hierarchy].option;options+=option;});var html="<select class='location level_"+level+"'>"+options+"</select>";var select=$(html);select.appendTo($('td.locationCell'));select.change(function(){var idContainer=that.getIdContainerHierarchy();var hierarchyPart=that.hierarchyMap[$('select.container',that.getBody()).val()][$(this).val()];if(hierarchyPart&&hierarchyPart.children){if(hierarchyPart.children.length>0){createCombos(hierarchyPart.children,hierarchyPart);}
else{getLocations(hierarchyPart);}}}).change();};function excelCol(intCol){if(intCol<=26){return String.fromCharCode(intCol+64);}
var reminder=intCol%26;var mod=parseInt(intCol/26,10);if(reminder==0){return excelCol(mod-1)+'Z';}
return excelCol(mod)+String.fromCharCode(reminder+64);}
function getLabel(ini,v){var numValue=parseInt(ini,10);v=parseInt(v,10);if(!isNaN(numValue)){return numValue+v;}
else{v=v+(ini.charCodeAt(0)-65);}
return excelCol(v+1);}
function getLocations(hierarchyPart){var idContainer=that.getIdContainerHierarchy();var locations=that.usedLocations[idContainer];var locationSettings=that.locationSettings[idContainer];var iniRow=locationSettings.ini_row;var iniCol=locationSettings.ini_col;var table=$("table.innerPicker",that.getBody());table.empty();var row=$("<tr><th>&nbsp;</th></tr>");for(var x=0;x<locationSettings.cols;x++){var headerCell=$("<th align='center'></th>");headerCell.html(getLabel(iniCol,x)+"");headerCell.appendTo(row);}
row.appendTo(table);for(var y=0;y<locationSettings.rows;y++){var row=$("<tr></tr>");$("<td>"+getLabel(iniRow,y)+"</td>").appendTo(row);for(var x=0;x<locationSettings.cols;x++){var cell=$("<td></td>");cell.attr('locRow',y);cell.attr('locCol',x);that.formatCell(cell,hierarchyPart,x,y);cell.appendTo(row);}
row.appendTo(table);}
that.markSelections(hierarchyPart.id_container_hierarchy);}
function buildDialog(j,onCompleteCallback,boxy_title){that.containers=j.containers;that.hierarchy=j.hierarchy;that.hierarchyMap=j.hierarchyMap;that.usedLocations=j.usedLocations;that.locationSettings=j.locationSettings;that.body=$(j.html);var confirmLabel=_("CONFIRM");var cancelLabel=_("CANCEL");var ifrm_quality=$('#ifrm_quality').length;if(ifrm_quality)
{onclick_str=" onclick='$(\"#ifrm_quality\").css(\"display\", \"block\");' ";}
else
{onclick_str=" onclick='$(\"#general\").css(\"display\", \"block\");' ";}
that.mainDialog=new Boxy(that.body,{title:boxy_title,modal:true,confirmHtml:"<img alt='"
+confirmLabel
+"' title='"
+confirmLabel
+"' id='saveConfirm' "
+onclick_str
+"src='../img/record_save_disabled.png'/>",closeText:"<img alt='"
+cancelLabel
+"' title='"
+cancelLabel
+"' "
+onclick_str
+"src='../img/record_cancel.png'/>",show:false,unloadOnHide:true});initSelection();setupEvents();showSelected();that.markSelections(that.getSelectedContainerHierarchy());$.ajaxSetup({async:true});if($.browser.msie&&$.browser.version=='6.0')
{if(ifrm_quality){$('#ifrm_quality').css('display','none');}else{$('#general').css('display','none');}}
that.mainDialog.show();if(onCompleteCallback){onCompleteCallback();}
that.updateSave();}
function showSelected(){var map=that.hierarchyMap[that.getIdContainer()];for(var key in map){var item=map[key];if(item){while(true){if(item&&item.children&&item.children.length>0){item=item.children[0];}else{break;}}}
break;}
for(var idContainerHierarchy in that.temporaryPageLocations){if(idContainerHierarchy!=item.id_container_hierarchy){var locations=that.temporaryPageLocations[idContainerHierarchy];for(var rowCol in locations){var loc=locations[rowCol];if(that.isThis(loc.id_lot,loc.id_strain)){var p=rowCol.split("_");var row=p[0];var col=p[1];var hierarchy=that.hierarchyMap[loc.id_container][idContainerHierarchy];if(!that.exceptionLocations[idContainerHierarchy+"_"+row+"_"+col]){that.addSelectedLocation(hierarchy,row,col,loc.quantity);}}}}}}
function initSelection(){$('select.container',that.getBody()).addFormattedOptions(that.containers,{value:'id_container',text:'description'});}
function setupEvents(){var c=$(that.getBody());$("#loading",c).hide();$("#loading",c).ajaxStart(function(){return that.ajaxStarted($(this));}).ajaxStop(function(){return that.ajaxStopped($(this));});that.createLocationSelects();$('select.container',c).change(function(){return that.containerChanged($(this));}).change();$('#saveConfirm').css('cursor','default');}}
function isEmptyObject(o){for(var p in o){if(o[p]!=o.constructor.prototype[p])
return false;}
return true;}
function cloneObject(obj){var c={};for(var i in obj){var prop=obj[i];if(typeof prop=='object'){c[i]=cloneObject(prop);}else{c[i]=prop;}}
return c;}