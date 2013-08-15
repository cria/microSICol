#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='preservation.form',
            category='main',
            js=('ext.jquery', 'ext.json', 'loc','ext.tinymce', 'data_div_manipulation','tinymce.init','loc_remove','form.default','feedback','form.preservation'),
            css=('location','location.default','preservation.default','default.form','default.detail','preservation.form')
           )
