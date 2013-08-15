#!/usr/bin/env python
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='ref.detail',
            category='main',
            js=('ext.jquery', 'data_div_manipulation','feedback'),
            css=('ref.default','default.detail')
           )
