#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

from os import path

#Page Headers
http_header = 'Content-type: text/html; charset=utf-8'
ajax_http_header = 'Content-type: text/plain; charset=utf-8'
javascript_line = '<script src="../js/%s.js" type="text/javascript"></script>'
css_line = '<link href="../css/%s.css" rel="stylesheet" type="text/css" media="all" />'

#System Directories
html_dir = 'html'
css_dir = 'css'
img_dir = 'img'
js_dir = 'js'
js_i18n_dir = path.join(js_dir, 'js_i18n')
lang_dir = 'lang'
py_dir = 'py'
sql_dir = 'sql'
po_dir = 'po'
session_dir = 'session'

#Others
session_file_extension = '.ini'
session_timeout = 60 * 30 #value in seconds
