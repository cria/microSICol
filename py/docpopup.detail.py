#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount( 
            page='docpopup.detail',
            category='main',
            js=(),
            css=('doc.default','default.detail')
           )

