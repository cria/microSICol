#!/usr/bin/env python 
#-*- coding: utf-8 -*-
  
#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='preferences',
            category='main',
            js=('ext.jquery', 'data_div_manipulation','form.default','feedback','form.preferences'),
            css=('preferences','default.detail')
           )
