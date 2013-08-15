#!/usr/bin/env python
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='ref.new',
            category='main',
            js=('ext.jquery', 'ext.tinymce','tinymce.init','form.ref','data_div_manipulation','form.default','feedback'),
            css=('ref.default','default.form','default.detail','ref.form')
           )
