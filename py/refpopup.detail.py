#!/usr/bin/env python 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='refpopup.detail',
            category='main',
            js=(),
            css=('ref.default','default.detail')
           )
