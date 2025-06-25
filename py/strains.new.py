#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount(
            page='strains.new',
            category='main',
            js=('ext.jquery', 'ext.sprintf', 'ext.json', 'loc','ext.tinymce','tinymce.init','form.strains','data_div_manipulation','autosuggest','form.strains.quality','form.strains.stock','form.default','feedback','strains.default'),
            css=('location','default','strains.default','default.form','default.detail','strains.form')
           )
# if __name__ == '__main__':
#      import timeit
#      t = timeit.Timer("""
# page = Principal()
# #Load Session (get from current logged-in user)
# page.cookie_value = 'c647330f658bd62aee82400b924425d3df90eb67'
# from modules.i18n import I18n
# page.i18n = I18n(cookie_value=page.cookie_value)
# page.mount(
#              page='strains.new',
#              category='main',
#              js=('ext.tinymce','tinymce.init','autosuggest','form.strains','data_div_manipulation','form.default','feedback'),
#              css=('strains.default','default.form','default.detail','strains.form')
#             )
# ""","from modules.page_mount import Principal")
#      print 'Time Elapsed = ' + str(min(t.repeat(5,1))) + ' seconds.'
#      raw_input()
