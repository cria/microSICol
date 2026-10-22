#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='import.data',
            category='main',
            js=None,
            css=None
           )