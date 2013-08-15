(function(){tinymce.PluginManager.requireLangPack('fieldlink');tinymce.create('tinymce.plugins.FieldLinkPlugin', {init:function(ed,url){var tlAware=false;var obj=document.getElementById(ed.id).parentNode;if (obj.nodeName.toUpperCase() != "P") {obj=obj.parentNode;}for(var i=0;i<obj.childNodes.length;i++){var ctrl=obj.childNodes[i];if (ctrl.nodeName.toUpperCase() == "IMG") {if (ctrl.getAttribute("src").indexOf("fieldlink") != -1) {tlAware=true;}}}if(tlAware){ed.addButton('fieldlink', {title: 'fieldlink.lang_fieldlink_button_desc',image: url + '/images/fieldlink.gif',cmd: 'mceFieldLink'});
ed.addCommand('mceFieldLink', function(one, incoming) {if(incoming){var sel_field=incoming.sel_field;var tl=null;switch(sel_field.options[sel_field.selectedIndex].value){case 'system':var sel_system=incoming.sel_system;tl = '[FIELD:'+sel_system.options[sel_system.selectedIndex].value+']';break;case 'report':var sel_report=incoming.sel_report;tl = '[FIELD:'+sel_report.options[sel_report.selectedIndex].value+']';break;}if(tl){
tinyMCE.execInstanceCommand(ed.id, 'mceInsertContent', true, tl, true);}}else {ed.windowManager.open({file : 'fieldlink.py',width : 355 + ed.getLang('example.delta_width', 0),height : 125 + ed.getLang('example.delta_height', 0),inline:1},{
editor_id:ed.id,sel_field : '',sel_system : '',sel_report:null});
}})
}},
createControl:function(n,cm){return null;},
getInfo:function(){return {longname: 'Sicol',author: 'Linear Softwares Matematicos',authorurl: 'http://www.linearsm.com.br',
infourl: '',version: tinyMCE.majorVersion + "." + tinyMCE.minorVersion};
}});
tinymce.PluginManager.add('fieldlink', tinymce.plugins.FieldLinkPlugin);})();
