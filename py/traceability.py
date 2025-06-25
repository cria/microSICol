#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#local imports
from .modules.page_mount import Principal

page = Principal()
page.mount(
    page='traceability',
    category='main',
    js=('form.default','feedback', 'traceability'),
    css=('traceability', 'default.form','default.lists', 'default.detail')
)
