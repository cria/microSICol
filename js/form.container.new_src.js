
$(function () {
	$("#demo").jstree({ 
		"xml_data" : {
			"data" : "" + 
						"<root>" + 
							"<item>" + 
								"<content><name><input type='text' style='display:none;' value='%root%' /></name></content>" + 
							"</item>" +													
						"</root>"						
						},
			"plugins" : [ "themes","xml_data","ui","crrm","cookies","search","types","hotkeys"],
			"types" : {
						"valid_children" : [ "root" ], //No node can be moved and became brother of the root.
						"default" : {}
	                }
							
	});
	$("#demo").bind("loaded.jstree", function (event, data) {
		data.inst.select_node('ul > li:first');
		$("#demo").find("ul:first").attr('id','Node_1');
		$('#Node_1').find("li:first").attr('id','Child_0');
	})

	$("#demo").bind('before.jstree', function(event, data)
	{
		if(data.plugin == 'crrm')
		{
			switch(data.func)
			{
				case('remove'):
					if(data.inst._get_parent(data.args[0])==-1)
					{		
						alert(_("The root node cannot be removed."));
						return false;
					}
				break;

				case('select_one'):
					data.inst.select_node($('#' + data.args[0])[0], true, event);
				break;
				
				default:
					break;
			}
		}
	});
});

$(function () { 
	$("#mmenu input").click(function () {
		switch(this.id) {
			case "add_root":
				$("#demo").jstree("create", 'root', "last", { "attr" : { "rel" : this.id.toString().replace("add_", "") } });
				break;
			
			case "add_folder":								
				$("#demo").jstree("create", null, "last", { "attr" : { "rel" : this.id.toString().replace("add_", "") } });								
				FormatarUltimoNivel('Node_1');	
				break;
			
			case "search":
				$("#demo").jstree("search", document.getElementById("text").value);
				break;
			
			case "text":
				break;
			
			case "select_one":
				//Demo selection of Node_2 son 2
				//$("#demo").jstree("select_one", 'Node_2','2');
				break;
			
			default:				
				$("#demo").jstree(this.id);
				var novoUl = $(lista[i]).find("ul")[0];
				FormatarUltimoNivel(novoUl.id);
				break;
		}
	});
});

function FormatarUltimoNivel(id)
{	
	var lista = $("ul[id|=" + id +"] > li");

	for (var i=0; i<lista.length; i++)
	{			
		if ($(lista[i]).find("input").val() != '%root%')
		{	
			if ($(lista[i]).find("ul").length > 0)
			{			
				$(lista[i]).find("input[objFinal*=Final]").css("display",'none');
				$(lista[i]).find("label[for*=Final]").css("display",'none');
				var novoUl = $(lista[i]).find("ul")[0];
				FormatarUltimoNivel(novoUl.id);			
			}
			else		
			{
				$(lista[i]).find("input[objFinal*=Final]").css("display",'block');
				$(lista[i]).find("label[for*=Final]").css("display",'block');
			}
		}
		else
		{
			var novoUl = $(lista[i]).find("ul")[0];
			FormatarUltimoNivel(novoUl.id);
		}
	}
}
