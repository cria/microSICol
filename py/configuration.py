#!/usr/bin/env python3  
#-*- coding: utf-8 -*-
  
#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount( 
            page='configuration',
            category='main',
            js=('configuration','ext.jquery','ext.tinymce','tinymce.init','data_div_manipulation','form.default','feedback', 'form.reports.step4'),
            css=('configuration','default.detail')
           )
