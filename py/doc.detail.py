#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount(
            page='doc.detail',
            category='main',
            js=('ext.jquery', 'data_div_manipulation','feedback'),
            css=('doc.default','default.detail')
           )
