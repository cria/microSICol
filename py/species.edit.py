#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount(
            page='species.form',
            category='main',
            js=('ext.jquery', 'ext.tinymce','tinymce.init','form.species','data_div_manipulation','form.default','feedback','sciname'),
            css=('species.default','default.form','default.detail')
           )
