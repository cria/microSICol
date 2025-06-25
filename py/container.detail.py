#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount( 
            page='container.detail',
            category='main',
            js=('feedback', 'jquery', 'jquery.cookie', 'jquery.hotkeys', 'jstree'),
            css=('default.detail', 'container.default', 'jstree')
           )
