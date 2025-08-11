#!/usr/bin/env python  
#-*- coding: utf-8 -*-
  
#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='strains.quality.list',
            category='external',
            js=('ext.jquery', 'ext.json', 'loc','form.strains.quality'),
            css=('location','configuration','default.detail', 'strains.form', 'strains.quality.default')
           )
