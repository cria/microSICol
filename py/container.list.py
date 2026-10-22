#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='container.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('container.list','default.lists', 'default.detail')
           )
