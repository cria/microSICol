#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='preservation.new',
            category='main',
            js=('ext.jquery','ext.json','ext.tinymce', 'data_div_manipulation','tinymce.init','loc','form.default','feedback','form.preservation'),
            css=('boxy','jquery.tooltip','location.default','preservation.default','default.form','default.detail','preservation.form')
           )
