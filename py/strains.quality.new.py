#!/usr/bin/env python  
#-*- coding: utf-8 -*-
  
#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='strains.quality.new',
            category='external',
            js=('ext.jquery', 'ext.json', 'loc','ext.tinymce', 'tinymce.init', 'form.default', 'form.strains.quality', 'feedback'),
            css=('location','configuration','default', 'default.detail', 'default.form', 'strains.form', 'strains.quality.default')
           )
