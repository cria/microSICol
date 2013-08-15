
var temporaryPageLocations={};var temporaryPageOriginalLocations={};var exceptionLocations={};var exceptionOriginalLocations={};var dados="";function setContainerStructure()
{anotherError=ObterDados($("#demo"));document.getElementsByName('complete_structure')[0].value=dados;return anotherError;}
function validateContainer(dateformat)
{errors=false;if(dados=="],")
{alert(_("Container must have at least an location data."));return-1;}
var select=$("select#preservation_method")[0];isEmpty(select,getLabel(select.name));var lista=$("input[type!='button']");for(var i=0;i<lista.length;i++)
{$(lista[i]).each(function()
{var label_name='';if($(this)[0].id.indexOf('Node')!=-1)
{label_name=$(this)[0].id.replace('Node','label');}
else
{label_name='label_'+$(this)[0].id;}
var label=$('#'+label_name)[0];var field=$(this)[0];if(!$(this).is(':hidden')&&!$(this).is(':disabled')&&$(this).val()=="")
{errors=true;showError(field,label,_("Field must not be empty."));}
else
{resetField(field,label);}});}
return errors;}
function ObterDados(objDiv)
{$(objDiv).find("ul:first").attr('id','Node_1');dados="";var anotherError="";var offspring=Prof('Child_0');if(offspring[1]>14)
{anotherError=-19;}
if(anotherError=="")
{if(offspring[0]==0)
{anotherError=-18;}}
if(anotherError=="")
{LerArvore('Node_1');}
return anotherError;}
function Prof(id)
{var no=$("li[id|="+id+"]"+" > ul");var ret=[1,0];if(no.length==0)
{return ret;}
else
{var lista=no.children("li");var tam=-1;for(var i=0;i<lista.length;i++)
{var item=Prof(lista[i].id);item[1]++;if(item[0]==0)
{ret[0]=0;}
if(tam==-1)
{tam=item[1];}
else{if(tam!=item[1])
{ret[0]=0;if(tam<item[1])
{tam=item[1];}}}}
ret[1]=tam;return ret;}}
function LerArvore(id)
{var lista=$("ul[id|="+id+"] > li");for(var i=0;i<lista.length;i++)
{if($(lista[i]).find("input").val()!='%root%')
{if($(lista[i]).find("input[objFinal|=Final1]").css("display")!='none')
{dados+="['"+$(lista[i]).find("input")[0].value+"|:|"+$(lista[i]).find("input")[1].value+"|:|"+$(lista[i]).find("input[objFinal|=Final1]").val()+"|-|"+$(lista[i]).find("input[objFinal|=Final2]").val()+"|-|"+$(lista[i]).find("input[objFinal|=Final3]").val()+"|-|"+$(lista[i]).find("input[objFinal|=Final4]").val()+"|-|"+$(lista[i]).find("input[objFinal|=Final5]").val()+"'";}
else
{dados+="['"+$(lista[i]).find("input")[0].value+"|:|"+$(lista[i]).find("input")[1].value+"|:|'";}}
if($(lista[i]).find("ul").length>0)
{if($(lista[i]).find("input").val()!='%root%')
{dados+=",";}
var novoUl=$(lista[i]).find("ul")[0];LerArvore(novoUl.id);}
dados+="],";}}