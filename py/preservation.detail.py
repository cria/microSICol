#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='preservation.detail',
            category='main',
            js=('ext.jquery', 'ext.json', 'loc', 'data_div_manipulation','feedback', 'open_popup'),
            css=('location', 'preservation.default','default.detail')
           )
