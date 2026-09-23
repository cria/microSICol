#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
    page='specieslink.list',
    category='main',
    js=('form.default','feedback'),
    css=('specieslink', 'default.form', 'default.detail')
)
