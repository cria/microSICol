#!/usr/bin/env python3  
#-*- coding: utf-8 -*-
  
#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='strains.quality.save',
            category='external',
            js=('ext.jquery', 'ext.tinymce', 'tinymce.init', 'form.default', 'form.strains.quality', 'feedback'),
            css=('default.detail','form.save')
           )
