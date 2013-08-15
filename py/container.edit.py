#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='container.form',
            category='main',
            js=('ext.jquery', 'ext.json', 'form.default','feedback', 'form.container','jquery', 'jquery.cookie', 'jquery.hotkeys', 'jstree'),  
            css=('container.default','default.detail','container.form','default.form','jstree')
           )
