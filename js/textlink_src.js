function init() { 
	tinyMCEPopup.resizeToInnerSize();
	//Start selectbox with _DOC_ option
	switch_fields('doc');
	//Start with first qualifier filtered
	doc_sel_q = document.getElementById('doc_sel_qualifier');
	filterDoc(doc_sel_q.options[doc_sel_q.selectedIndex].value);
}

function cancelAction() {
	tinyMCEPopup.close();
}

function insertTextLink()
{
	sel_field = document.getElementById('sel_field').value;
	switch (sel_field)
	{
		case "ref":
			if (!document.getElementById('ref_sel_ref').length)
			{
				alert(_("Please, select a reference."));
				return false;
			}
			break;
		case "doc":
			if (!document.getElementById('doc_sel_doc').length) 
			{
				alert(_("Please, select a document."));
				return false;
			}
			break;
	}
	
	// Insert TextLink in tinyMCE textarea
	tinyMCEPopup.execCommand('mceTextLink', false, { 
		sel_field : document.getElementById('sel_field'),
		doc_sel_doc : document.getElementById('doc_sel_doc'),
		ref_sel_ref : document.getElementById('ref_sel_ref'),
		link_text_link : document.getElementById('link_text_link'),
		link_title_link : document.getElementById('link_title_link'),
		tax_text_tax : document.getElementById('tax_text_tax'),
		win : window
		}, false);

  //Close tinyMCE popup
	tinyMCEPopup.close();
	return false;
}

function switch_fields(tl_type)
{
  switch(tl_type)
  {
    case "ref":
    	document.getElementById('middle_one').innerHTML = _("Reference");
    	document.getElementById('right_one').innerHTML = '&nbsp;';
    	document.getElementById('third_column').style.display = 'none';
    	document.getElementById('ref_ref').style.display = '';
    	document.getElementById('link_link').style.display = 'none';
    	document.getElementById('link_title').style.display = 'none';
    	document.getElementById('doc_doc').style.display = 'none';
    	document.getElementById('doc_qualifier').style.display = 'none';
    	document.getElementById('tax_tax').style.display = 'none';
      break;
    case "doc":
    	document.getElementById('middle_one').innerHTML = _("Qualifier");
    	document.getElementById('right_one').innerHTML = _("Document");
    	document.getElementById('third_column').style.display = '';
    	document.getElementById('ref_ref').style.display = 'none';
    	document.getElementById('link_link').style.display = 'none';
    	document.getElementById('link_title').style.display = 'none';
    	document.getElementById('doc_doc').style.display = '';
    	document.getElementById('doc_qualifier').style.display = '';
    	document.getElementById('tax_tax').style.display = 'none';
      break;
    case "link":
    	document.getElementById('middle_one').innerHTML = _("Link");
    	document.getElementById('right_one').innerHTML = _("Title");
    	document.getElementById('third_column').style.display = '';
    	document.getElementById('ref_ref').style.display = 'none';
    	document.getElementById('link_link').style.display = '';
    	document.getElementById('link_title').style.display = '';
    	document.getElementById('doc_doc').style.display = 'none';
    	document.getElementById('doc_qualifier').style.display = 'none';
    	document.getElementById('tax_tax').style.display = 'none';
    	break;
    case "tax":
    	document.getElementById('middle_one').innerHTML = _("Taxon");
    	document.getElementById('right_one').innerHTML = '&nbsp;';
    	document.getElementById('third_column').style.display = 'none';
    	document.getElementById('ref_ref').style.display = 'none';
    	document.getElementById('link_link').style.display = 'none';
    	document.getElementById('link_title').style.display = 'none';
    	document.getElementById('doc_doc').style.display = 'none';
    	document.getElementById('doc_qualifier').style.display = 'none';
    	document.getElementById('tax_tax').style.display = '';
      break;
  }
}

var global_docs = null;

function filterDoc(doc_type)
{ 
  doc_sel = document.getElementById('doc_sel_doc');
  if (global_docs == null) //save "select" field to be filtered
  {
    global_docs = doc_sel.cloneNode(true);
  }
  //Clear "select"
  doc_sel.innerHTML = "";
  //Insert only filtered values
  for(var i=0;i < global_docs.length;i++)
  {
    if (global_docs.options[i].getAttribute('qualifier') == doc_type)
    {
      var option = document.createElement("option");
      option.text = global_docs.options[i].text;
      option.value = global_docs.options[i].value;
      doc_sel.options.add(option);
    } 
  }
}
