#!/usr/bin/env python  
#-*- coding: utf-8 -*-
  
#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='strains.stock.list',
            category='external',
            js=('ext.jquery', 'form.strains.stock'),
            css=('stock.default','default.detail', 'default.form')
           )
