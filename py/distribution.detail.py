#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='distribution.detail',
            category='main',
            js=('ext.jquery', 'ext.json', 'loc', 'data_div_manipulation','feedback', 'open_popup'),
            css=('location', 'distribution.default','default.detail')
           )
