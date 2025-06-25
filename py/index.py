#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Content-Type: text/html")
print()
import os
print("CWD:", os.getcwd())

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='tests',
            category='others',
            js='tests',
            css='tests'
           )
