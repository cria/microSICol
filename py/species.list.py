#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='species.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('species.list','species.default','default.lists')
           )
