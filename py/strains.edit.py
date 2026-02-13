#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='strains.form',
            category='main',
            js=('ext.jquery', 'ext.sprintf', 'ext.json', 'loc', 'ext.tinymce','tinymce.init','form.strains','data_div_manipulation','autosuggest','form.strains.quality','form.strains.stock','form.default','feedback','strains.default'),
            css=('location','default','strains.default','default.form','default.detail','strains.form')
           )
