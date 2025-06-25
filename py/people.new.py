#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount(
            page='people.new',
            category='main',
            js=('ext.jquery', 'ext.tinymce','tinymce.init','contact_relations_manipulation','form.people','data_div_manipulation','form.default','feedback'),
            css=('people.default','default.form','default.detail')
          )
