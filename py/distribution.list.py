#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='distribution.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('distribution.list','distribution.default','default.lists')
           )
