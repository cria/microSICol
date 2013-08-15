
var multi_language_fields=new Array();multi_language_fields.push("comments");multi_language_fields.push("ambient_risk");var default_multi_language_fields=new Array();default_multi_language_fields.concat(multi_language_fields);default_multi_language_fields.push("comments");default_multi_language_fields.push("ambient_risk");var mapTextArea=new Object();mapTextArea['taxon_ref']=65535;mapTextArea['ambient_risk_*']=65535;mapTextArea['hazard_group_ref']=65535;mapTextArea['comments_*']=65535;mapTextArea['synonym']=65535;var init=true;function validateSpecies()
{applySciName();errors=false;form=document.getElementsByName('edit')[0];taxon_group=document.getElementsByName('taxon_group')[0];lbl_taxon_group=getLabel('taxon_group');resetField(taxon_group,lbl_taxon_group);if(!isValidTextArea('taxon_ref',65535))errors=true;if(!isValidTextArea('hazard_group_ref',65535))errors=true;if(!isValidTextArea('synonym',65535))errors=true;langs=document.getElementById('data_langs').value;langs=langs.split(',');for(mlf in multi_language_fields)
{if(mlf!='remove')
{max_size=mapTextArea[multi_language_fields[mlf]+'_*'];for(lang in langs)
{if(lang!='remove')
{if(!isValidTextArea(multi_language_fields[mlf]+'_'+langs[lang],max_size))errors=true;}}}}
if(isEmpty(taxon_group,lbl_taxon_group))errors=true;if(!validateSciNameFields())errors=true;return errors;}
function checkTaxonGroup()
{var sel=document.getElementById('taxon_group');var current_group=sel.options[sel.selectedIndex].value;if(current_group=='2'||current_group=='3')
{loadPossibleAltStates();document.getElementById('alt_state_table').style.display="block";if(!init)
{document.getElementById('p_alt_state_type').style.display="none";document.getElementById('alt_state_type').selectedIndex=0;}}
else
{document.getElementById('alt_state_table').style.display="none";document.getElementById('p_alt_state_type').style.display="none";document.getElementById('alt_state').selectedIndex=0;document.getElementById('alt_state_type').selectedIndex=0;}
displaySciNameBuilder();}
function checkAltState()
{var sel=document.getElementById('alt_state');if(sel.selectedIndex>=0){var current_group=sel.options[sel.selectedIndex].value;if(current_group!='')
{document.getElementById('p_alt_state_type').style.display="block";}
else
{document.getElementById('p_alt_state_type').style.display="none";document.getElementById('alt_state_type').selectedIndex=0;}}}
function loadPossibleAltStates()
{var taxon_group=document.getElementById('taxon_group');var alt_state=document.getElementById('alt_state');alt_state.length=0;alt_state.options[alt_state.length]=new Option("","");for(var i=0;i<window.alternate_states.length;i++)
{if(taxon_group.options[taxon_group.selectedIndex].value==window.alternate_states[i][0])
{alt_state.options[alt_state.length]=new Option(window.alternate_states[i][2],window.alternate_states[i][1]);if(init&&document.getElementById("id_alt_states").value==window.alternate_states[i][1])
{alt_state.options[alt_state.length-1].selected=true;}}}
init=false;}
function disableLinks()
{disableMenu(document.getElementById('menu'),document.getElementById('active_species'));disableLink(document.getElementById('active_preferences'));disableLink(document.getElementById('active_configuration'));disableLink(document.getElementById('active_utilities'));}
function checkAltStateTemp()
{setTimeout("checkAltState()",200)}
addEvent(window,'load',checkTaxonGroup);addEvent(window,'load',checkAltStateTemp);addEvent(window,'load',disableLinks);