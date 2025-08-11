#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='reports.save',
            category='main',
            js=None,
            css=('default.detail','form.save')
           )