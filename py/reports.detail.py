#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='reports.detail',
            category='main',
            js=('ext.jquery', 'data_div_manipulation','feedback', 'form.default','ext.json', 'form.reports','form.reports.step3'),
            css=('reports.default','default.detail', 'reports.form')
           )
