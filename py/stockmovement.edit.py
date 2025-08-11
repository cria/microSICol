#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='stockmovement.form',
            category='main',
            js=('ext.jquery', 'ext.json', 'form.default','feedback', 'form.stockmovement', 'loc'),
            css=('stockmovement.default','default.form','default.detail', 'stockmovement.form','boxy','location.default')
           )
