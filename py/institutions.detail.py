#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='institutions.detail',
            category='main',
            js=('ext.jquery', 'data_div_manipulation','feedback'),
            css=('institutions.default','default.detail')
           )
