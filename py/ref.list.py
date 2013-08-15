#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='ref.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('ref.list','ref.default','default.lists')
           )