#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='institutions.form',
            category='main',
            js=('ext.jquery', 'ext.tinymce','tinymce.init','form.institutions','data_div_manipulation','form.default','feedback'),
            css=('institutions.form','institutions.default','default.form','default.detail')
           )
