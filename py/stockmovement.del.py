#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='stockmovement.del',
            category='main',
            js=None,
            css=('default.detail','form.save')
           )
