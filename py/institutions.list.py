#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='institutions.list',
            category='main',
            js=('filter_lists','feedback'),
            css=('institutions.list','institutions.default','default.lists')
           )