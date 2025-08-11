#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='people.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('people.list','people.default','default.lists')
           )