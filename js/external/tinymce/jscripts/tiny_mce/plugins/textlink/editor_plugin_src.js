/**
 * $Id: editor_plugin_src.js 201 2007-02-12 15:56:56Z spocke $
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2007, Moxiecode Systems AB, All rights reserved.
 */

(function() {
    tinymce.PluginManager.requireLangPack('textlink');

    tinymce.create('tinymce.plugins.TextLinkPlugin', {
        init: function(ed, url){
            var tlAware = false;
            
            var obj = document.getElementById(ed.id).parentNode;
            if (obj.nodeName.toUpperCase() != "P") {
                obj = obj.parentNode;
            }
            
            for (var i = 0; i < obj.childNodes.length; i++) {
                var ctrl = obj.childNodes[i];
                if (ctrl.nodeName.toUpperCase() == "IMG") {
                    if (ctrl.getAttribute("src").indexOf("textlink") != -1) {
                        tlAware = true;
                    } 
                }
            }
            
            if (tlAware) {
                ed.addButton('textlink', {
                    title: 'textlink.lang_textlink_button_desc',
                    image: url + '/images/textlink.gif',
                    cmd: 'mceTextLink'
                });
                
                ed.addCommand('mceTextLink', function(one, incoming) {
                    if (incoming) {
                        var sel_field = incoming.sel_field;
                        var tl = null;
                        switch (sel_field.options[sel_field.selectedIndex].value) {
                            case 'doc':
                                var sel_doc = incoming.doc_sel_doc;
                                tl = '[DOC:'+sel_doc.options[sel_doc.selectedIndex].value+']';
                                break;
                            
                            case 'link':
                                var link = incoming.link_text_link.value;
                                var title = incoming.link_title_link.value;
                                if (title == '')
                                {
                                title = link;
                                }
                                tl = '[LINK:' + title + '|' + link + ']';
                                break;
                            
                            case 'ref':
                                var sel_ref = incoming.ref_sel_ref;
                                tl = '[REF:' + sel_ref.options[sel_ref.selectedIndex].value + ']';
                                break;
                            
                            case 'tax':
                                tl = '[TAX:' + incoming.tax_text_tax.value + ']';
                                break;
                        }
                        
                        if (tl) {
                            tinyMCE.execInstanceCommand(ed.id, 'mceInsertContent', true, tl, true);
                        }
                    }
                    else {
                        ed.windowManager.open({
                            file : 'textlink.py',
                            width : 355 + ed.getLang('example.delta_width', 0),
                            height : 125 + ed.getLang('example.delta_height', 0),
                            inline : 1
                        }, {
                            editor_id : ed.id, // Plugin absolute URL
                            sel_field : '',
                            doc_sel_doc : '',
                            ref_sel_ref : null,
                            link_text_link : null,
                            link_title_link : null,
                            tax_text_tax : null
                        });                 
                    }
                })
            }
        },
        
        createControl: function(n, cm){
            return null;
        },
        
        getInfo: function(){
            return {
                longname: 'Sicol',
                author: 'Linear Softwares Matematicos',
                authorurl: 'http://www.linearsm.com.br',
                infourl: '',
                version: tinyMCE.majorVersion + "." + tinyMCE.minorVersion
            };
        }
    });

    tinymce.PluginManager.add('textlink', tinymce.plugins.TextLinkPlugin);
})();