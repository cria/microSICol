#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

#local imports
from modules.page_mount import Principal

page = Principal()
page.mount(
            page='tests',
            category='others',
            js='tests',
            css='tests'
           )
