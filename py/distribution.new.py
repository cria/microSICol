#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='distribution.new',
            category='main',
            js=('ext.jquery', 'ext.json', 'loc','ext.tinymce','tinymce.init','form.distribution','data_div_manipulation','form.default','feedback'),
            css=('location','distribution.default','default.form','default.detail','distribution.form')
          )
