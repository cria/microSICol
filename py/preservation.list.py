#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='preservation.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('preservation.list','preservation.default','default.lists')
           )
