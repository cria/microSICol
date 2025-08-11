#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount( 
            page='distribution.form',
            category='main',
            js=('ext.jquery','ext.json','ext.tinymce','tinymce.init','loc','form.distribution','data_div_manipulation','form.default','feedback'),
            css=('boxy','jquery.tooltip','distribution.form','location.default','distribution.default','default.form','default.detail')
           )
