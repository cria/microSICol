#!/usr/bin/env python
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='reports.new',
            category='main',
            js=('ext.jquery','ext.jquery.ui','ext.jquery.ui.sortable','ext.tinymce','tinymce.init','form.reports','form.reports.step2','form.reports.step4','data_div_manipulation','form.default','feedback', 'form.reports.step3','strains.default'),
            css=('reports.form','reports.form.step2','reports.form.step3','reports.default','default.form','default.detail','jquery.ui.all')
           )