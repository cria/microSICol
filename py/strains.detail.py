#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='strains.detail',
            category='main',
            js=('ext.jquery', 'ext.json', 'loc','data_div_manipulation','feedback', 'form.strains.quality', 'form.strains.stock', 'strains.default', 'open_popup'),
            css=('location','strains.default','default.detail', 'strains.form')
           )
