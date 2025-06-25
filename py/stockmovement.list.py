#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount(
            page='stockmovement.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('stockmovement.list','stockmovement.default','default.lists', 'default.detail')
           )