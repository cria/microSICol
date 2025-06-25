#!/usr/bin/env python3  
#-*- coding: utf-8 -*-
  
#local imports
from .modules.page_mount import Principal
#from dbgp.client import brk

page = Principal()
#brk(host="localhost", port=9000)
page.mount( 
            page='fieldlink',
            category='main',
            js=('fieldlink','form.default','feedback'),
            css=('default.detail', 'dialog')
           )
