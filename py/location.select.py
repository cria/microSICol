#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='location',
            category='main',
            js=('ext.jquery', 'ext.json', 'form.default','loc','feedback'),
            css=('boxy','location.default','default.form','default.detail')
           )
