
$(function(){$("ul.droptrue").sortable({connectWith:"ul"});$("ul.dropfalse").sortable({connectWith:"ul",dropOnEmpty:false});$("#total").sortable({receive:function(event,ui){if($("#select li").size()>0||$("#total li").size()>1)
{$(ui.sender).sortable('cancel');}
if($("#total li").size()==1)
{resetField(document.getElementById("total"),document.getElementById("label_total"));resetField(document.getElementById("select"),document.getElementById("label_select"));}}});$("#select").sortable({receive:function(event,ui){if($("#total li").size()>0||$("#select li").size()>300)
{$(ui.sender).sortable('cancel');}
if($("#select li").size()==1)
{resetField(document.getElementById("total"),document.getElementById("label_total"));resetField(document.getElementById("select"),document.getElementById("label_select"));}}});$("#group").sortable({receive:function(event,ui){if($("#group li").size()>5)
{$(ui.sender).sortable('cancel');}}});});function generate_data()
{var field="";var select="";var group="";var total="";$("#field li").each(function(){field+=$(this).attr('id')+",";});$("#select li").each(function(){select+=$(this).attr('id')+",";});$("#group li").each(function(){group+=$(this).attr('id')+",";});$("#total li").each(function(){total+=$(this).attr('id')+",";});if(field!="")
{field="'"+field.substring(0,(field.length-1))+"'";}
if(select!="")
{select="'"+select.substring(0,(select.length-1))+"'";}
if(group!="")
{group="'"+group.substring(0,(group.length-1))+"'";}
if(total!="")
{total="'"+total.substring(0,(total.length-1))+"'";}
$('#hdn_field').val(field);$('#hdn_select').val(select);$('#hdn_group').val(group);$('#hdn_total').val(total);}