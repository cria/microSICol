#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='doc.new',
            category='main',
            js=('ext.jquery', 'ext.tinymce','tinymce.init','form.doc_','data_div_manipulation','form.default','feedback'),
            css=('doc.form','doc.default','default.form','default.detail')
           )
