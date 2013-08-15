/**
 * $Id: editor_plugin_src.js 201 2007-02-12 15:56:56Z spocke $
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2007, Moxiecode Systems AB, All rights reserved.
 */

tinyMCE.importPluginLanguagePack('textlink');

var TinyMCE_TextLinkPlugin = {
	getInfo : function() {
		return {
			longname : 'Sicol',
			author : 'Linear Softwares Matematicos',
			authorurl : 'http://www.linearsm.com.br',
			infourl : '',
			version : tinyMCE.majorVersion + "." + tinyMCE.minorVersion
		};
	},

	initInstance : function (inst) {
	},

	getControlHTML : function (cn) {
		switch (cn) {
		  //Insert TextLink button image 
			case "textlink" :
          //Check whether there is any TextLink Image telling this is a TextLink-aware form element
          //Go to parent node and search for "img" element
          obj = document.getElementById(tinyMCE.getSicolId(tinyMCE.getEditorId())).parentNode;
          if (obj.nodeName.toUpperCase() != "P") obj = obj.parentNode; //special case: when we have multilanguage textareas
          tl_aware = false;
          for (var i=0; i < obj.childNodes.length; i++)
          {
              if (obj.childNodes[i].nodeName.toUpperCase() == "IMG")
              {
                if (obj.childNodes[i].getAttribute('src').indexOf("textlink") != -1)
                  tl_aware = true;
              }
          }
			    if (tl_aware) return tinyMCE.getButtonHTML(cn, 'lang_textlink_button_desc', '{$pluginurl}/images/textlink.gif','mceTextLink', true);
		}

		return "";
	},

	execCommand : function (editor_id, element, command, user_interface, value) {
		var inst = tinyMCE.getInstanceById(editor_id), selectedText = inst.selection.getSelectedText();

		function defValue(key, default_value) {
			value[key] = typeof(value[key]) == "undefined" ? default_value : value[key];
		}

		if (!value) value = [];

		defValue("editor_id", editor_id);
		defValue("sel_field", '');
		defValue("doc_sel_doc", '');
		defValue("ref_sel_ref", null);
		defValue("link_text_link", null);
		defValue("link_title_link", null);
		defValue("tax_text_tax", null);

		switch (command) 
    {
			case "mceTextLink" :
			  //If user_interface = True, then show an user interface
				if (user_interface) {
					var template = new Array();

					template['file'] = '../../../../../../../py/textlink.py';
					template['width'] = 355;
					template['height'] = 125 + (tinyMCE.isNS7 ? 20 : 0) + (tinyMCE.isMSIE ? 15 : 0);

					inst.selection.collapse(true);
					tinyMCE.openWindow(template, value);
				} 
        else //When popup is closed 
        {
					if (value['sel_field'] != '')
					{
					  sel_field = value['sel_field']; 
					  switch (sel_field.options[sel_field.selectedIndex].value)
					  {
					     case 'doc':
					       sel_doc = value['doc_sel_doc'];
					       tl = '[DOC:'+sel_doc.options[sel_doc.selectedIndex].value+']';
       					 tinyMCE.execInstanceCommand(editor_id,'mceInsertContent',true,tl,true);
					       break;
					     case 'link':
       					 tl = '[LINK:'+value['link_text_link'].value;
       					 if (value['link_title_link'].value != '') tl += '|'+value['link_title_link'].value;
       					 tl += ']';
       					 tinyMCE.execInstanceCommand(editor_id,'mceInsertContent',true,tl,true);
					       break;
					     case 'ref':
					       sel_ref = value['ref_sel_ref'];
       					 tl = '[REF:'+sel_ref.options[sel_ref.selectedIndex].value+']';
       					 tinyMCE.execInstanceCommand(editor_id,'mceInsertContent',true,tl,true);
					       break;
					     case 'tax':
       					 tl = '[TAX:' + value['tax_text_tax'].value + ']';
       					 tinyMCE.execInstanceCommand(editor_id,'mceInsertContent',true,tl,true);
					       break;
            }
          }
				}
				return true;
		} //end of switch
		return false;
	}
};

tinyMCE.addPlugin("textlink", TinyMCE_TextLinkPlugin);
