#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='species.new',
            category='main',
            js=('ext.jquery', 'ext.json', 'loc', 'ext.tinymce','tinymce.init','form.species','data_div_manipulation','form.default','feedback','sciname'),
            css=('species.default','default.form','default.detail')
           )
