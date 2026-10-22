#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='container.new',
            category='main',
            js=('ext.jquery', 'ext.json', 'form.default','feedback', 'form.container', 'form.container.new', 'jquery', 'jquery.cookie', 'jquery.hotkeys', 'jstree'),
            css=('container.default','default.detail', 'container.form', 'jstree', 'default.form')
           )
