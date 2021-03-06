function stripHTMLComments(element_id, html, body) {
    /* strip HTML comments */
    html = html.replace(/<!--[\S\s]*?-->/g, '');

    return html;
}

tinymce.EditorManager.init({mode:"specific_textareas",editor_selector:"mceEditor",valid_elements:"a[href|target=_blank],div[align],b/strong,i/em,p,sup,sub,u,br",language:__tinyMCE_lang,entity_encoding:"raw",theme:"advanced",preformatted:true,theme_advanced_toolbar_location:"top",theme_advanced_statusbar_location:"none",theme_advanced_toolbar_align:"left",theme_advanced_buttons1:"bold,italic,underline,sub,sup,charmap,separator,undo,redo,separator,link,unlink,separator,cleanup,removeformat,help,textlink,fieldlink",theme_advanced_buttons2:"",theme_advanced_buttons3:"",plugins:"fieldlink,textlink",onblur_callback:"tinyMCE_onblur()",save_callback:"stripHTMLComments"});
