#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='people.form',
            category='main',
            js=('ext.jquery', 'ext.tinymce','tinymce.init','form.people','data_div_manipulation','contact_relations_manipulation','form.default','feedback'),
            css=('people.default','default.form','default.detail')
           )
