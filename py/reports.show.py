#!/usr/bin/env python3  
#-*- coding: utf-8 -*-
  
#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='reports.show',
            category='main',
            js=('ext.jquery', 'ext.sprintf', 'ext.json', 'loc', 'ext.tinymce','tinymce.init','data_div_manipulation','feedback', 'form.default'),
            css=('reports.default','default.detail', 'reports.form', 'form.save')
           )
