#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='stockmovement.detail',
            category='main',
            js=('feedback'),
            css=('default.detail', 'stockmovement.default')
           )
